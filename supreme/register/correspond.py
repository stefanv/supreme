import numpy as np

import supreme.config
log = supreme.config.get_log(__name__)

from supreme.geometry import Grid
from logpolar import patch_match

def _safe_coord(i, j, img, win_size):
    """Return the coordinates of a window only if
    it fits inside the image."""
    hwin = (win_size - 1) / 2

    m = i - hwin
    n = i + hwin + 1
    p = j - hwin
    q = j + hwin + 1
    if (m < 0) or (n >= img.shape[0]) or \
       (p < 0) or (q >= img.shape[1]):
        raise IndexError("Patch crosses image boundary")
    else:
        return m, n, p, q

def correspond(fA, A, fB, B, win_size=9):
    """Given coordinates of features in two images, determine
    possible correspondences.

    Parameters
    ----------
    fA : list of tuple (x,y)
        Coordinates of the features in the source image.
    A : (m,n) ndarray of type uint8
        Source image.
    fB : list of tuple (x,y)
        Coordinates of the features in the target image.
    A : (m,n) ndarray of type uint8
        Target image.

    Returns
    -------
    matches : list
        [((coord_source), (coord_target)), ...]

    """
    # Ensure uneven window size
    win_size = int(win_size)
    win_size = win_size + ((win_size + 1) % 2)

## Used to round feature corners, used e.g. in the DPT
##     # Mask for removing corners
##     r_max = ((win_size - 1) / 2.)**2
##     g = Grid(win_size, win_size)
##     center = (win_size - 1)/ 2.
##     mask = (((g['cols'] - center)**2 + (g['rows'] - center)**2) > r_max)

    # Pre-calculate patches
    pA = {}
    angles = np.linspace(-np.pi, np.pi, 50)
    for (i, j) in fA:
        try:
            m, n, p, q = _safe_coord(i, j, A, win_size)
        except IndexError:
            pass
        else:
            patch = A[m:n, p:q]
            # patch[mask] = 0 # round feature
            pA[(i, j)] = patch

    pB = {}
    for (i, j) in fB:
        try:
            m, n, p, q = _safe_coord(i, j, B, win_size)
        except IndexError:
            pass
        else:
            patch = B[m:n, p:q]
            # patch[mask] = 0 # round feature
            pB[(i, j)] = patch

    count = 1
    result_d = {}

    for (i, j) in fA:
        if count % 10 == 1:
            log.debug("%s/%s" % (count, len(fA)))
        count += 1
        match_likelihood = -np.inf

        patch_A = pA.get((i, j), None)
        if patch_A is None:
            continue

        # Normalise values
        patch_A = patch_A - patch_A.mean()

        # Sort values for QQ-comparison
        patch_A = np.sort(patch_A)

        for (m, n) in fB:
            patch_B = pB.get((m, n), None)
            if patch_B is None:
                continue
            patch_B = np.sort(patch_B - patch_B.mean())

            norm = np.linalg.norm

            # A very counter-intuitive feature-matching scheme
            # that works.

            # |A - B| <= max(|A|, |B|) since all elements are positive
            tmp = patch_B - patch_A
            tmp = -norm(tmp) / max(norm(patch_B), norm(patch_A))

            if tmp > -0.5 and tmp > match_likelihood:
                match_likelihood = tmp
                result_d[(i, j)] = (m, n)

    # Get rid of features that occur twice in the mapping
    # There can be only one, after all
    reverse_d = {}
    for k, v in result_d.iteritems():
        reverse_d[v] = reverse_d.get(v, [])
        reverse_d[v].append(k)

    for k, v in reverse_d.iteritems():
        if len(v) > 1:
            for coord in v:
                del result_d[coord]

    return result_d.items()
