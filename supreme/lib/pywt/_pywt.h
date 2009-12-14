#ifndef __PYX_HAVE___pywt
#define __PYX_HAVE___pywt
#ifdef __cplusplus
#define __PYX_EXTERN_C extern "C"
#else
#define __PYX_EXTERN_C extern
#endif

/* "/private/tmp/trunk/src/_pywt.pyx":147
 *     return __wfamily_list_long[:]
 * 
 * cdef public class Wavelet [type WaveletType, object WaveletObject]:             # <<<<<<<<<<<<<<
 *     """
 *     Wavelet(name, filter_bank=None) object describe properties of
 */

struct WaveletObject {
  PyObject_HEAD
  Wavelet *w;
  PyObject *name;
  PyObject *number;
};

#ifndef __PYX_HAVE_API___pywt

__PYX_EXTERN_C DL_IMPORT(PyTypeObject) WaveletType;

#endif

PyMODINIT_FUNC init_pywt(void);

#endif
