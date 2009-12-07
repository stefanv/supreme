#cython: cdivision=True
# -*- python -*-

__all__ = ['connected_regions', 'decompose', 'reconstruct']

import numpy as np

cimport numpy as np

import cython
import sys

from ccomp import label
from connected_region cimport ConnectedRegion

cimport connected_region_handler as crh
cimport int_array as iarr
cimport stdlib
from int_array cimport IntArray

def connected_regions(np.ndarray[np.int_t, ndim=2] img):
    """Return ConnectedRegions that, together, compose the whole image.

    Parameters
    ----------
    img : ndarray
        Input image.

    Returns
    -------
    labels : ndarray
        `img`, labeled by connectivity.
    c : dict
        Dictionary of ConnectedRegions, indexed by label value.

    """
    cdef int rows = img.shape[0]
    cdef int columns = img.shape[1]

    cdef ConnectedRegion cr, cur_region

    # perform initial labeling
    cdef np.ndarray[np.int_t, ndim=2] labels = label(img)

    cdef dict regions = {}

    # create the first level components
    cdef int r = 0, c = 0, connect_from, prev_label = 0, cur_label = 0

    for r in range(rows):
        connect_from = 0

        for c in range(1, columns + 1):
            prev_label = labels[r, c - 1]

            if c < columns:
                cur_label = labels[r, c]
            else:
                cur_label = prev_label

            # Different region or end of row reached
            if prev_label != cur_label or c == columns:

                # New region?
                if prev_label > len(regions) - 1:
                    regions[prev_label] = ConnectedRegion(
                        shape=(rows, columns),
                        value=img[r, connect_from],
                        start_row=r,
                        rowptr=[0])

                cur_region = regions[prev_label]

                # New row?
                if crh._current_row(cur_region) != r:
                    crh._new_row(cur_region)

                # Add connected region
                iarr.append(cur_region.colptr, connect_from)
                iarr.append(cur_region.colptr, c)

                connect_from = c

    # finalise rows
    for cr in regions.itervalues():
        crh._new_row(cr)
        cr._nnz = crh.nnz(cr)

    return labels, regions

cdef _merge_all(dict merges, dict regions, int area, dict regions_by_area,
                np.int_t* labels, int rows, int cols):
    """
    Merge all regions that have connections on their boundaries.

    """
    cdef ConnectedRegion cr_a, cr_b
    cdef int idx0, idx1, a_label, b_label

    for idx0 in merges:
        a_label = labels[idx0]
        cr_a = regions[a_label]

        for idx1 in merges[idx0]:
            b_label = labels[idx1]
            cr_b = regions[b_label]

            # Always merge a region with a larger index into a
            # region with a smaller index.  This results in an ordered
            # connected component labelling.
            if b_label < a_label:
                cr_a, cr_b = cr_b, cr_a
                a_label, b_label = b_label, a_label

            # Regions have alreay been merged
            if b_label == a_label:
                continue

            # Merge; update regions, labels
            # Image has already been updated in identify_pulses_and_merges
            del regions[b_label]
            crh._set_array(labels, rows, cols, cr_b, a_label)

            # If we merge a larger region with a smaller region,
            # we have to update the regions_by_area, since that
            # area will still be visited.

            if cr_b._nnz >= area:
                (<set>regions_by_area[cr_b._nnz]).remove(cr_b)
            if cr_a._nnz >= area:
                (<set>regions_by_area[cr_a._nnz]).remove(cr_a)

            # Update labels of cr_b
            crh.merge(cr_a, cr_b) # merge b into a

            try:
                (<set>regions_by_area[cr_a._nnz]).add(cr_a)
            except KeyError:
                regions_by_area[cr_a._nnz] = set([cr_a])

cdef dict _identify_pulses_and_merges(set regions, int area, dict pulses,
                                      np.int_t* img_data, np.int_t* labels,
                                      int rows, int cols, int* workspace,
                                      int mode=0):
    """Save pulses of this area, and return regions that need to be merged.

    Parameters
    ----------
    mode : int
        0 - U (upper), raise minima
        1 - L (lower), lower maxima
        2 - B (both), do both

    Returns
    -------
    merges : dict
        {idx: [cr0_idx, cr1_idx, ...]}

        idx is the index (row*max_cols + col) of the current region
        cr0, cr1, ... are the indices of the connected_regions with which it
                      must be merged

    """
    cdef ConnectedRegion cr, cr_save

    cdef int b_max
    cdef int b_min
    cdef int old_value

    cdef dict merges = {}
    cdef list merge_indices = []
    cdef IntArray y, x
    cdef int i, idx0, idx1
    cdef int xi, yi
    cdef bool do_merge

    if area not in pulses:
        pulses[area] = []

    for cr in regions:
        idx0 = cr._start_row * cols + cr.colptr.buf[0]
        old_value = cr._value
        do_merge = False

        y, x = crh._outside_boundary(cr, workspace)

        # Upper
        if mode == 0 or mode == 2:
            b_min = crh._boundary_minimum(x, y, img_data, rows, cols)

            # Minimal set
            if b_min > old_value: # Note that this needs to be strictly
                                  # greater than.  It may happen that,
                                  # during the lowering of values further down,
                                  # the connected regions end up being equal.
                cr._value = b_min
                do_merge = True

        # Lower
        if mode == 1 or mode == 2:
            b_max = crh._boundary_maximum(x, y, img_data, rows, cols)

            # Maximal set
            if b_max < old_value:
                cr._value = b_max
                do_merge = True

        # Minimal or maximal region detected
        if do_merge:
            # This should occur exactly once: on the last
            # pulse that covers the whole image
            if cr._value == -1:
                cr._value = 0

            # By setting the region value here, we prevent neighbouring
            # regions from picking it up in consequent iterations of this
            # loop
            crh._set_array(img_data, rows, cols, cr, cr._value)
            merge_indices = []

            cr_save = crh.copy(cr)
            cr_save._value = old_value - cr._value # == pulse height
            (<list>pulses[area]).append(cr_save)

            for i in range(x.size):
                xi = x.buf[i]
                yi = y.buf[i]

                if (xi < 0) or (xi >= cols) or (yi < 0) or (yi >= rows):
                    # Position outside boundary
                    continue

                idx1 = yi * cols + xi

                if img_data[idx1] == cr._value:
                    merge_indices.append(idx1)

            merges[idx0] = merge_indices

    if len(pulses[area]) == 0:
        del pulses[area]

    return merges

def decompose(np.ndarray[np.int_t, ndim=2] img):
    """Decompose a two-dimensional signal into pulses.

    Parameters
    ----------
    img : 2-D ndarray of ints
        Input signal.

    Returns
    -------
    pulses : dict
        Dictionary of ConnectedRegion objects, indexed by pulse area.

    See Also
    --------
    reconstruct

    """
    img = img.copy()

    cdef np.ndarray[np.int_t, ndim=2] labels
    cdef dict regions

    cdef ConnectedRegion cr
    cdef int nz

    cdef np.int_t* img_data = <np.int_t*>img.data
    cdef int max_rows = img.shape[0]
    cdef int max_cols = img.shape[1]

    # labels (array): `img`, numbered according to connected region
    # regions (dict): ConnectedRegions, indexed by label value.
    labels, regions = connected_regions(img)
    cdef np.int_t* labels_data = <np.int_t*>labels.data

    cdef set merge_region_positions
    cdef int* workspace = <int*>stdlib.malloc(sizeof(int) * (max_cols + 2) * 3)

    cdef dict pulses = {}

    cdef int old_value, levels, percentage_done, percentage

    cdef dict regions_by_area = {}
    for cr in regions.itervalues():
        try:
            regions_by_area[cr._nnz].add(cr)
        except KeyError:
            regions_by_area[cr._nnz] = set([cr])

    levels = max_cols * max_rows + 1
    percentage_done = 0

    sys.stdout.flush()
    for area in range(levels):
        percentage = area*100/levels
        if percentage != percentage_done:
            sys.stdout.flush()
            percentage_done = percentage

        # Upper
        if not area in regions_by_area:
            continue

        merges = \
               _identify_pulses_and_merges(regions_by_area[area], area, pulses,
                                           img_data, labels_data,
                                           max_rows, max_cols, workspace, 0)

        _merge_all(merges, regions, area, regions_by_area,
                   labels_data, max_rows, max_cols)

        # Lower
        if not area in regions_by_area:
            continue

        merges = \
               _identify_pulses_and_merges(regions_by_area[area], area, pulses,
                                           img_data, labels_data,
                                           max_rows, max_cols, workspace, 1)

        _merge_all(merges, regions, area, regions_by_area,
                   labels_data, max_rows, max_cols)

        del regions_by_area[area]


    stdlib.free(workspace)
    return pulses

def reconstruct(dict regions, tuple shape, int min_area=-1, int max_area=-1):
    """Reconstruct an image from the given connected regions / pulses.

    Parameters
    ----------
    regions : dict
        Impulses indexed by area.  This is the output of `decompose`.
    shape : tuple
        Shape of the output image.
    min_area, max_area : int
        Impulses with areas in [min_area, max_area] are used for the
        reconstruction.

    Returns
    -------
    out : ndimage
        Reconstructed image.
    areas : 1d ndarray
        Pulses with these areas occur in the image.
    area_count : 1d ndarray
        For each area in the above list, there are this many impulses.

    """
    cdef ConnectedRegion cr

    cdef np.ndarray[np.int_t, ndim=2] out = np.zeros(shape, dtype=int)

    if max_area == -1:
        max_area = out.shape[0] * out.shape[1] + 1

    if min_area == -1:
        min_area = 0

    cdef list areas = []
    cdef list area_count = []
    cdef int a

    for a in regions:
        if a >= min_area and a <= max_area:
            areas.append(a)
            area_count.append(0)

            area_count[-1] += len(regions[a])

            for cr in regions[a]:
                crh._set_array(<np.int_t*>out.data, out.shape[0], out.shape[1],
                               cr, cr._value, 1)

    areas_arr, area_count_arr = np.array(areas), np.array(area_count)

    # Sort by area
    ind = np.argsort(areas_arr)
    areas_arr = areas_arr[ind]
    area_count_arr = area_count_arr[ind]

    return out, areas, area_count_arr
