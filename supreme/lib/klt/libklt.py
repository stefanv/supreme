import numpy as N
from ctypes import c_int, c_uint8, c_float, c_double, c_char, \
                   Structure, POINTER, pointer, c_void_p

from numpy.testing import set_local_path, restore_path
set_local_path('../../..')
import supreme.config as SC
from supreme.ext import array_1d_double, array_2d_double, array_1d_int, \
                        array_2d_int, array_1d_uchar, array_2d_uchar, \
                        atype
restore_path()

_lib = N.ctypeslib.load_library('libklt_',__file__)

class TrackingContext(Structure):
    _fields_ = [
        ('mindist', c_int),
        ('window_width', c_int),
        ('window_height', c_int),
        ('sequentialMode', c_int),
        ('smoothBeforeSelecting', c_int),
        ('writeInternalImages', c_int),
        ('lighting_insensitive', c_int),
        ('min_eigenvalue', c_int),
        ('min_determinant', c_float),
        ('min_displacement', c_float),
        ('max_iterations', c_int),
        ('max_residue', c_float),
        ('grad_sigma', c_float),
        ('smooth_sigma_fact', c_float),
        ('pyramid_sigma_fact', c_float),
        ('nSkippedPixels', c_int),
        ('borderx', c_int),
        ('bordery', c_int),
        ('nPyramidLevels', c_int),
        ('subsampling', c_int),
        ('pyramid_last', c_void_p),
        ('pyramid_last_gradx', c_void_p),
        ('pyramid_last_grady', c_void_p)]

    def __init__(self):
        tc = _lib.KLTCreateTrackingContext()
        for (attrib,type) in self._fields_:
            self.__setattr__(attrib, tc.contents.__getattribute__(attrib))
        _lib.KLTFreeTrackingContext(tc)

    def __str__(self):
        rep = 'Tracking context:\n'
        for (attrib,value) in self._fields_:
            rep += '    ' + \
                   ("%s = %s\n" % (attrib, str(self.__getattribute__(attrib))))
        return rep

class FloatImage(Structure):
    _fields_ = [
        ('ncols', c_int),
        ('nrows', c_int),
        ('data', POINTER(c_float))]

class Feature(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('val', c_int),
        ('aff_img', POINTER(FloatImage)),
        ('aff_img_gradx', POINTER(FloatImage)),
        ('aff_img_grady', POINTER(FloatImage)),
        ('aff_x', c_float),
        ('aff_y', c_float),
        ('aff_Axx', c_float),
        ('aff_Ayx', c_float),
        ('aff_Axy', c_float),
        ('aff_Ayy', c_float)]

class FeatureList(Structure):
    _fields_ = [
        ('nFeatures', c_int),
        ('feature', POINTER(POINTER(Feature)))]

    def __init__(self, n):
        self._features = (Feature*n)(*[Feature() for f in range(n)])
        self._features_p = (POINTER(Feature)*n)(*[pointer(f) for f in self._features])
        self.feature = pointer(self._features_p[0])
        self.nFeatures = n

    def __iter__(self):
        for i in range(self.nFeatures):
            yield self.feature[i].contents

    def __len__(self):
        return self.nFeatures

    def __str__(self):
        rep = ''
        for i,f in enumerate(self):
            rep += 'Feature #%d:  (%f,%f) with value of %d\n' % \
                       (i, f.x, f.y, f.val)
        return rep


class FeatureHistory(Structure):
    _fields_ = [
        ('nFrames', c_int),
        ('feature', POINTER(Feature))]

class FeatureTable(Structure):
    _fields_ = [
        ('nFrames', c_int),
        ('nFeatures', c_int),
        ('feature', POINTER(Feature))]

PixelType = c_uint8

libklt_api = {
   'KLTSelectGoodFeatures' : (None,
                              [POINTER(TrackingContext), array_2d_uchar,
                               c_int, c_int, POINTER(FeatureList)]),
   'KLTTrackFeatures' : (None,
                         [POINTER(TrackingContext), array_2d_uchar,
                          array_2d_uchar, c_int, c_int,
                          POINTER(FeatureList)]),
   'KLTReplaceLostFeatures' : (None,
                               [POINTER(TrackingContext), array_2d_uchar,
                                c_int, c_int, POINTER(FeatureList)]),
   'KLTCreateTrackingContext' : (POINTER(TrackingContext),[]),
   'KLTFreeTrackingContext' : (None,[POINTER(TrackingContext)]),
   }

def register_api(lib,api):
    import inspect
    parent_frame = inspect.currentframe().f_back
    for f, (restype, argtypes) in api.iteritems():
        func = getattr(lib, f)
        func.restype = restype
        func.argtypes = argtypes
        parent_frame.f_locals[f] = func

register_api(_lib,libklt_api)

def select_good_features(tracking_context, img, features):
    img, = atype(img, N.uint8)
    rows,cols = img.shape
    _lib.KLTSelectGoodFeatures(tracking_context, img, cols, rows, features)

def track_features(tracking_context, img1, img2, features):
    img1, img2 = atype([img1,img2],[N.uint8,N.uint8])
    rows,cols = img1.shape
    _lib.KLTTrackFeatures(tracking_context, img1, img2,
                          cols, rows, features)

def replace_lost_features(tracking_context, img, features):
    img, = atype(img,N.uint8)
    rows,cols = img.shape
    _lib.KLTReplaceLostFeatures(tracking_context, img, cols, rows, features)
