/*      $Id: cPolygon.c,v 1.32 2005/08/12 13:48:39 joerg Exp $   */

#include <math.h>
#include <float.h>
#include <string.h>
#include <Python.h>
#include "gpc.h"
#include "PolyUtil.h"

#ifdef SYSTEM_WIN32
#include <malloc.h>
#endif /*SYSTEM_WIN32*/

#define POLY_AUTHOR \
"Author:   Joerg Raedler, dezentral gbr Berlin. software@dezentral.de\n\
Homepage: http://www.dezentral.de/soft/\n\n\
Polygon is based on gpc, which was developed by Alan Murta, the gpc homepage\n\
is at: http://www.cs.man.ac.uk/aig/staff/alan/software/ "

#define POLY_LICENSE \
"The Polygon package itself covered by the GNU LGPL, please look at \n\
http://www.gnu.org/copyleft/lesser.html for details.\n\n\
Polygon is based on gpc, which is free for non-commercial usage only.\n\
If you wish to use Polygon in a commercial project, please look at the gpc\n\
homepage and contact the author of gpc.\n\n\
gpc is a great piece of software, you should support the author and respect\n\
his license statment:\n\
    \"This library is provided free of charge for non-commercial users. Reaching\n\
    its current state took up almost two years of personal development effort.\n\
    If you have found this software to be useful for your purposes please make\n\
    a donation and help support the continuation of this project. Thanks!\""

#define DOCSTR_POLY_MODULE \
"cPolygon - this module is part of the Polygon \n\
package. The most interesting thing here is a type called Polygon."

#define DOCSTR_POLY_TYPE \
"Polygon - a type to represent a polygon. In this module a polygon is a \n\
collection of contours, each contour may be normal or a hole inside \n\
other contours. \n\
\n\
The initialisation arguments may be:\n\
- another Polygon instance which will be cloned, or\n\
- a string or file object which will be read, or\n\
- a sequence of points which will be used as the first normal contour.\n\
A point is a sequence of two floats.\n\
\n\
Operations on polygons:\n\
(to be continued...)"

#define STYLE_TUPLE 0
#define STYLE_LIST  1
#define STYLE_ARRAY 2

#ifndef DEFAULT_STYLE
#define DEFAULT_STYLE STYLE_LIST
#endif

#ifdef WITH_NUMERIC
#include <Numeric/arrayobject.h>
#endif

#define STRBUF_MAX 300
#define DNDEF DBL_MAX
#define INDEF INT_MAX

#ifdef GPC_EPSILON
/* GPC_EPSILON is constant and may not be changed! */
#define CONST_EPSILON
#else
/* GPC_EPSILON is a variable and may be changed! */
extern double GPC_EPSILON;
#endif
#ifndef POLYVERSION
#define POLYVERSION 0.0
#endif

static int dataStyle = DEFAULT_STYLE;

/* general Exception */
static PyObject *PolyError;

/* some common exceptions ... */
#define ERR_ARG PolyError, "Wrong number or type of arguments"
#define ERR_INV PolyError, "Invalid polygon or contour for operation"
#define ERR_IND PyExc_IndexError, "Index out of range for contour/strip"
#define ERR_MEM PyExc_MemoryError, "Out of memory"
#define ERR_TYP PyExc_TypeError, "Invalid type of operand"

/* raise an exception and return NULL */
static PyObject *Polygon_Raise(PyObject *e, char *msg) {
    PyErr_SetString(e, msg);
    return NULL;
}

/***************************  Polygon ********************************/

/* Polygon */
typedef struct {
    PyObject_HEAD
    PyObject *attr;
    gpc_polygon *p;
    double boundingBox[4];
    int bbValid;
} Polygon;

staticforward PyTypeObject    Polygon_Type;
staticforward PyMethodDef     Polygon_Methods[24];
staticforward PyNumberMethods Polygon_NumberMethods;
staticforward PySequenceMethods Polygon_SequenceMethods;


#define Polygon_Check(o) ((o)->ob_type == &Polygon_Type)


static Polygon *Polygon_NEW(void *ptr) {
    Polygon *obj = PyObject_NEW(Polygon, &Polygon_Type);
    if (ptr != NULL)
        /* create from existing gpc_polygon struct */
        obj->p = (gpc_polygon *)ptr;
    else {
        /* create a new struct */
        if (! (obj->p = poly_p_new()))
            return (Polygon *)Polygon_Raise(ERR_MEM);
    }
    obj->bbValid = 0;
    obj->attr = NULL;
    return obj;
}


/* gets (cached) boundingbox or calculates and caches */
static void Polygon_getBoundingBox(Polygon *p, double *x0, double *x1, double *y0, double *y1) {
    if (p->bbValid) {
        *x0 = p->boundingBox[0];
        *x1 = p->boundingBox[1];
        *y0 = p->boundingBox[2];
        *y1 = p->boundingBox[3];
    } else {
        poly_p_boundingbox(p->p, x0, x1, y0, y1);
        p->boundingBox[0] = *x0;
        p->boundingBox[1] = *x1;
        p->boundingBox[2] = *y0;
        p->boundingBox[3] = *y1;
        p->bbValid = 1;
    }
}


static void Polygon_dealloc(Polygon *self) {
    gpc_free_polygon(self->p);
    free(self->p);
    Py_XDECREF(self->attr);
    PyMem_Del(self);
}

#define DOCSTR_POLY_WRITE \
"write(file)\n\
arguments:\n\
  - a writable file object\n\
  - or a filename string\n\
returns: None\n\
Writes Polygon data to a file in gpc format."
static PyObject *Polygon_write(Polygon *self, PyObject *args) {
    PyObject *O;
    int hflag = 1;
    if (! PyArg_ParseTuple(args, "O|i", &O, &hflag))
        return Polygon_Raise(ERR_ARG);
    if (PyFile_Check(O))
        gpc_write_polygon(PyFile_AsFile(O), hflag, self->p);
    else if (PyString_Check(O)) {
        FILE *f = fopen(PyString_AsString(O), "w");
        if (!f)
            return Polygon_Raise(PyExc_IOError, "Could not open file for writing!");
        gpc_write_polygon(f, hflag, self->p);
        fclose(f);
    } else
        return Polygon_Raise(ERR_ARG);
    Py_INCREF(Py_None);
    return Py_None;
}

#define DOCSTR_POLY_READ \
"read(file)\n\
arguments:\n\
  - a readable file object\n\
  - or a filename string\n\
returns: None\n\
Reads Polygon data from a file in gpc format."
static PyObject *Polygon_read(Polygon *self, PyObject *args) {
    PyObject *O;
    int hflag = 1;
    if (! PyArg_ParseTuple(args, "O|i", &O, &hflag))
        return Polygon_Raise(ERR_ARG);
    if (PyFile_Check(O))
        gpc_read_polygon(PyFile_AsFile(O), hflag, self->p);
    else if (PyString_Check(O)) {
        FILE *f = fopen(PyString_AsString(O), "r");
        if (!f)
            return Polygon_Raise(PyExc_IOError, "Could not open file for reading!");
        gpc_read_polygon(f, hflag, self->p);
        fclose(f);
    } else
        return Polygon_Raise(ERR_ARG);
    Py_INCREF(Py_None);
    return Py_None;
}


#define DOCSTR_POLY_ADDCONTOUR \
"addContour(c |, hole=0)\n\
arguments:\n\
  - pointlist\n\
  - and an optional hole flag\n\
returns: None\n\
Add a contour (outline or hole)."
static PyObject *Polygon_addContour(Polygon *self, PyObject *args) {
#ifdef WITH_NUMERIC
    PyObject *a=NULL;
    gpc_vertex_list *vl;
    int hole = 0;
    if (! PyArg_ParseTuple(args, "O|i", &a, &hole))
        return Polygon_Raise(ERR_ARG);
    if ((a = PyArray_ContiguousFromObject(a, PyArray_DOUBLE, 2, 2)) == NULL)
        return Polygon_Raise(ERR_ARG);
    if (((PyArrayObject *)a)->nd != 2)            return Polygon_Raise(ERR_ARG);
    if (((PyArrayObject *)a)->dimensions[1] != 2) return Polygon_Raise(ERR_ARG);
    vl = PyMem_New(gpc_vertex_list, 1);
    vl->num_vertices = ((PyArrayObject *)a)->dimensions[0];
    vl->vertex = PyMem_New(gpc_vertex, vl->num_vertices);
    memcpy((vl->vertex), (((PyArrayObject *)a)->data), 2*vl->num_vertices*sizeof(double));
    Py_DECREF(a);
#else
    PyObject *list=NULL, *flist, *point=NULL, *X, *Y;
    gpc_vertex_list *vl;
    gpc_vertex *v;
    int i, imax, hole = 0;
    if (! PyArg_ParseTuple(args, "O|i", &list, &hole))
        return Polygon_Raise(ERR_ARG);
    if (! PySequence_Check(list))
        return Polygon_Raise(ERR_ARG);
    flist = PySequence_Fast(list, "this is not a sequence");
    if ((! flist) || ((imax = PySequence_Length(flist)) <= 2))
        return Polygon_Raise(ERR_INV);
    vl = PyMem_New(gpc_vertex_list, 1);
    vl->num_vertices = imax;
    vl->vertex = v = PyMem_New(gpc_vertex, imax);
    for (i=0; i<imax; i++) {
        point = PySequence_Fast(PySequence_Fast_GET_ITEM(flist, i), "this is not a point");
        if ((!point) || (PySequence_Length(point) != 2))
            return Polygon_Raise(ERR_INV);
        v->x = PyFloat_AsDouble(X = PyNumber_Float(PySequence_Fast_GET_ITEM(point, 0)));
        v->y = PyFloat_AsDouble(Y = PyNumber_Float(PySequence_Fast_GET_ITEM(point, 1)));
        v++;
        Py_DECREF(X);
        Py_DECREF(Y);
        Py_DECREF(point);
    }
    Py_DECREF(flist);
#endif /* WITH_NUMERIC */
    gpc_add_contour(self->p, vl, hole);
    self->bbValid = 0;
    PyMem_Free(vl->vertex);
    PyMem_Free(vl);
    Py_INCREF(Py_None);
    return Py_None;
}


static PyObject *Polygon_new(PyObject *self, PyObject *args) {
    PyObject *O = NULL, *TMP = NULL;
    int hole = 0;
    Polygon *p = Polygon_NEW(NULL);
    if (! PyArg_ParseTuple(args, "|Oi", &O, &hole))
        Polygon_Raise(ERR_ARG);
    if (O != NULL) {
        if ((PyTypeObject *)PyObject_Type(O) == &Polygon_Type) {
            if (poly_p_clone(((Polygon *)O)->p, p->p) != 0) {
                Polygon_dealloc(p);
                return Polygon_Raise(ERR_MEM); 
            }
        } else if (PyString_Check(O)) {
            TMP = Polygon_read(p, args);
        } else if (PySequence_Check(O)) {
            TMP = Polygon_addContour(p, args);
        } else if (PyFile_Check(O)) {
            TMP = Polygon_read(p, args);
        } else return Polygon_Raise(ERR_ARG);
        if (TMP) Py_DECREF(TMP);
        if (PyErr_Occurred()) {
            Polygon_dealloc(p);
            return NULL;
        }
    }
    return (PyObject *)p;
}


static PyObject *Polygon_repr(PyObject *self) {
    char buf[STRBUF_MAX];
    int i, j;
    gpc_polygon * p = ((Polygon *)self)->p;
    gpc_vertex_list *vl;
    gpc_vertex *v;
    PyObject * s = PyString_FromString("Polygon:");
    vl = p->contour;
    for(i=0; i<p->num_contours; i++) {
        if (*((p->hole)+i) == 0) 
            sprintf(buf, "\n  <%d:Contour:", i);
        else
            sprintf(buf, "\n  <%d:Hole   :", i);
        PyString_ConcatAndDel(&s, PyString_FromString(buf));
        v = vl->vertex;
        for (j = 0; j < vl->num_vertices; j++) {
            sprintf(buf, " [%d:%#.2g, %#.2g]", j, v->x, v->y);
            PyString_ConcatAndDel(&s, PyString_FromString(buf));
            v++;
        }
        PyString_ConcatAndDel(&s, PyString_FromString(">"));
        vl++;
    }
    return s;
}


static int Polygon_len(PyObject *self) {
    return ((Polygon *)self)->p->num_contours;
}


static PyObject *Polygon_getitem(PyObject *self, int item) {
    PyObject *R;
    gpc_vertex_list * vl = NULL;
    gpc_vertex *v;
    int i, imax;
    gpc_polygon *p = ((Polygon *)self)->p;
    if (item < 0) item += p->num_contours;
    if ((item >= p->num_contours) || (item < 0))
        return Polygon_Raise(ERR_IND);
    vl = (p->contour)+item;
    imax = vl->num_vertices;
    switch (dataStyle) {
        case STYLE_TUPLE: {
            PyObject *XY;
            v = vl->vertex;
            R = PyTuple_New(imax);
            for (i=0; i < imax; i++) {
                XY = PyTuple_New(2);
                PyTuple_SetItem(XY, 0, PyFloat_FromDouble(v->x));
                PyTuple_SetItem(XY, 1, PyFloat_FromDouble(v->y));
                PyTuple_SetItem(R, i, XY);
                v++;
            }
        } break;
        case STYLE_LIST: {
            PyObject *XY;
            v = vl->vertex;
            R = PyList_New(imax);
            for (i=0; i < imax; i++) {
                XY = PyTuple_New(2);
                PyTuple_SetItem(XY, 0, PyFloat_FromDouble(v->x));
                PyTuple_SetItem(XY, 1, PyFloat_FromDouble(v->y));
                PyList_SetItem(R, i, XY);
                v++;
            }
        } break;
#ifdef WITH_NUMERIC
        case STYLE_ARRAY: {
            int dims[2] = {0, 2};
            PyArrayObject *a;
            dims[0] = imax; 
            R = PyArray_FromDims(2, dims, PyArray_DOUBLE);
            a = (PyArrayObject *)R;
            memcpy(a->data, vl->vertex, sizeof(gpc_vertex)*vl->num_vertices);
        } break;
#endif /* WITH_NUMERIC */
        default:
            return Polygon_Raise(PolyError, "Unknown data style");
    }
    return Py_BuildValue("O", R);
}


#define DOCSTR_POLY_CONTOUR \
"contour(i)\n\
argument:\n\
  contour index\n\
returns:\n\
  a contour as tuple of  2-tuples\n\
Gives  the contour with index i."
static PyObject *Polygon_getContour(Polygon *self, PyObject *args) {
    int item;
    if (!PyArg_ParseTuple(args, "i", &item))
        return Polygon_Raise(ERR_ARG);
    return Polygon_getitem((PyObject *)self, item);
}


#define DOCSTR_POLY_SIMPLIFY \
"simplify()\n\
arguments: None\n\
returns: None\n\
Try to simplify Polygon. It's possible to add overlapping contours or holes \n\
which are outside of  other contours. This may result in wrong calculations \n\
of the area, center point, bounding box or other values. Call this method to \n\
make sure the Polygon is in a good shape. The method first adds all contours \n\
with a hole flag of 0, then substracts all holes and replaces the original \n\
Polygon  with the result."
static PyObject *Polygon_simplify(Polygon *self, PyObject *args) {
    gpc_polygon *ret, *lop, *rop, *tmp, *p = self->p;
    int i;
    if (p->num_contours <= 0) {
        Py_INCREF(Py_None);
        return Py_None;
    }
    if (! (lop = poly_p_new())) return Polygon_Raise(ERR_MEM);
    if (! (rop = poly_p_new())) return Polygon_Raise(ERR_MEM);
    if (! (ret = poly_p_new())) return Polygon_Raise(ERR_MEM);
    /* find first contour which is not a hole */
    i = 0;
    while ((i < p->num_contours) && (p->hole[i] == 1))
        i++;
    if (i < p->num_contours) 
        gpc_add_contour(lop, p->contour+i, 1);
    /* then try to add other contours */
    for (i++; i < p->num_contours; i++) {
        if (p->hole[i] == 0) {
            gpc_free_polygon(rop);
            gpc_free_polygon(ret);
            gpc_add_contour(rop, (p->contour+i), 0);
            gpc_polygon_clip(GPC_UNION, lop, rop, ret); 
            tmp = lop;
            lop = ret;
            ret = tmp;
        }
    }
    /* then try to cut out holes */
    for (i = 0; i < p->num_contours; i++) {
        if (p->hole[i] == 1) {
            gpc_free_polygon(rop);
            gpc_free_polygon(ret);
            gpc_add_contour(rop, (p->contour+i), 0);
            gpc_polygon_clip(GPC_DIFF, lop, rop, ret); 
            tmp = lop;
            lop = ret;
            ret = tmp;
        }
    }
    gpc_free_polygon(self->p);
    free(self->p);
    self->p = lop;
    gpc_free_polygon(ret);
    free(ret);
    gpc_free_polygon(rop);
    free(rop);
    self->bbValid = 0;
    return Py_BuildValue("O", Py_None);
}


#define DOCSTR_POLY_SHIFT \
"shift(xs, ys)\n\
arguments: two shift values for x and y\n\
returns: None\n\
Shifts the polygon by adding xs and ys."
static PyObject *Polygon_shift(Polygon *self, PyObject *args) {
  double x, y;
  if (! PyArg_ParseTuple(args, "dd", &x, &y))
      return Polygon_Raise(ERR_ARG);
  if ((x != 0.0) || (y != 0.0))
      poly_p_shift(self->p, x, y);
  self->bbValid = 0;
  return Py_BuildValue("O", Py_None);
}


#define DOCSTR_POLY_SCALE \
"scale(xs, ys |, xc, yc)\n\
arguments:\n\
  - two scaling  values for x and y direction\n\
  - and optional two floats for the center point\n\
returns: None\n\
Scales the polygon by multiplying with xs and ys around the center point. \n\
If no center is given  the center point of the bounding box is used, which \n\
will not be changed by this operation."
static PyObject *Polygon_scale(Polygon *self, PyObject *args) {
  double xs, ys, xc=DNDEF, yc=DNDEF;
  if (! PyArg_ParseTuple(args, "dd|dd", &xs, &ys, &xc, &yc))
      return Polygon_Raise(ERR_ARG);
  if ((xs != 1.0) || (ys != 1.0)) {
      if (xc == DNDEF) {
          double x0, x1, y0, y1;
          Polygon_getBoundingBox(self, &x0, &x1, &y0, &y1);
          xc = 0.5 * (x0+x1);
          yc = 0.5 * (y0+y1);
      }
      poly_p_scale(self->p, xs, ys, xc, yc);
  }
  self->bbValid = 0;
  return Py_BuildValue("O", Py_None);
}


#define DOCSTR_POLY_ROTATE \
"rotate(a |, xc, yc)\n\
arguments:\n\
  - an angle (float)\n\
  - and optional two floats for the center point\n\
returns: None\n\
Rotates the polygon by angle a around center point in ccw direction. If no \n\
center is given the center point of the bounding box is used."
static PyObject *Polygon_rotate(Polygon *self, PyObject *args) {
  double alpha, xc=DNDEF, yc=DNDEF;
  if (! PyArg_ParseTuple(args, "d|dd", &alpha, &xc, &yc))
      return Polygon_Raise(ERR_ARG);
  if (alpha != 0.0) {
      if (xc == DNDEF) {
          double x0, x1, y0, y1;
          Polygon_getBoundingBox(self, &x0, &x1, &y0, &y1);
          xc = 0.5 * (x0+x1);
          yc = 0.5 * (y0+y1);
      }
      poly_p_rotate(self->p, alpha, xc, yc);
  }
  self->bbValid = 0;
  return Py_BuildValue("O", Py_None);
}


#define DOCSTR_POLY_WARPTOBOX \
"warpToBox(x0, x1, y0, y1)\n\
arguments: four floats to specify the corners of the new bounding box\n\
returns: None\n\
Scales and shifts the polygon to fit into the bounding box specified by \n\
x0, x1, y0 and y1. Make sure: x0<x1 and y0<y1"
static PyObject *Polygon_warpToBox(Polygon *self, PyObject *args) {
  double x0, x1, y0, y1;
  if (! PyArg_ParseTuple(args, "dddd", &x0, &x1, &y0, &y1))
      return Polygon_Raise(ERR_ARG);
  if (self->bbValid)
      poly_p_warpToBox(self->p, x0, x1, y0, y1, self->boundingBox);
  else
      poly_p_warpToBox(self->p, x0, x1, y0, y1, NULL);
  self->bbValid = 0;
  return Py_BuildValue("O", Py_None);
}


#define DOCSTR_POLY_FLIP \
"flip(|x)\n\
agument: optional x value\n\
returns: None\n\
Flips polygon in x direction. If a value for x is not given, the center of \n\
the bounding box is used."
static PyObject *Polygon_flip(Polygon *self, PyObject *args) {
  double x = DNDEF;
  if (! PyArg_ParseTuple(args, "|d", &x))
      return Polygon_Raise(ERR_ARG);
  if (x == DNDEF) {
      double x0, x1, y0, y1;
      Polygon_getBoundingBox(self, &x0, &x1, &y0, &y1);
      x = 0.5 * (x0+x1);
  } else
      self->bbValid = 0;
  poly_p_flip(self->p, x);
  return Py_BuildValue("O", Py_None);
}


#define DOCSTR_POLY_FLOP \
"flop(|y)\n\
argument: optional y value\n\
returns: None\n\
Flips polygon in y direction. If a value for y is not given, the center of \n\
the bounding box is used."
static PyObject *Polygon_flop(Polygon *self, PyObject *args) {
  double y = DNDEF;
  if (! PyArg_ParseTuple(args, "|d", &y))
      return Polygon_Raise(ERR_ARG);
  if (y == DNDEF) {
      double x0, x1, y0, y1;
      Polygon_getBoundingBox(self, &x0, &x1, &y0, &y1);
      y = 0.5 * (y0+y1);
  } else
      self->bbValid = 0;
  poly_p_flop(self->p, y);
  return Py_BuildValue("O", Py_None);
}


#define DOCSTR_POLY_NPOINTS \
"nPoints(|i)\n\
argument: optional contour index\n\
returns: an integer\n\
Returns the number of points of one contour or of the whole polygon. Is much \n\
faster than len(p[i]) or reduce(add, map(len, p))!"
static PyObject *Polygon_nPoints(Polygon *self, PyObject *args) {
  int i=INDEF, n=0;
  if (! PyArg_ParseTuple(args, "|i", &i))
      return Polygon_Raise(ERR_ARG);
  if (i!=INDEF) {
      if ((i >= 0) && (i < self->p->num_contours))
          return Py_BuildValue("i",  self->p->contour[i].num_vertices);
      else 
          return Polygon_Raise(ERR_IND);
  }
  for (i=0; i < self->p->num_contours; i++) n += self->p->contour[i].num_vertices;
  return Py_BuildValue("i", n);
}


#define DOCSTR_POLY_AREA \
"area(|i)\n\
argument: optional  contour index\n\
returns: a float\n\
Calculates the area of one contour (when called with index) or of the whole \n\
polygon. All values are positive! The polygon area is the sum of areas of all \n\
solid contours minus the sum of all areas of holes."
static PyObject *Polygon_area(Polygon *self, PyObject *args) {
  int i=INDEF;
  if (! PyArg_ParseTuple(args, "|i", &i))
      return Polygon_Raise(ERR_ARG);
  if (i!=INDEF) {
      if ((i >= 0) && (i < self->p->num_contours))
          return Py_BuildValue("d", poly_c_area(self->p->contour+i));
      else 
          return Polygon_Raise(ERR_IND);
  }
  return Py_BuildValue("d",  poly_p_area(self->p));
}


#define DOCSTR_POLY_ORIENTATION \
"orientation(|i)\n\
argument: optional contour index\n\
returns: single integer or list of integers: \n\
  1 for ccw, -1 for cw, 0 for invalid contour.\n\
Calculates the orientation of one contour (when called with index) or of all \n\
contours. There's no default orientation, holes are defined by the hole flag, \n\
not by the orientation!"
static PyObject *Polygon_orientation(Polygon *self, PyObject *args) {
  int i=INDEF;
  if (! PyArg_ParseTuple(args, "|i", &i))
      return Polygon_Raise(ERR_ARG);
  if (i!=INDEF) {
      if ((i >= 0) && (i < self->p->num_contours))  
          return Py_BuildValue("i", poly_c_orientation(self->p->contour+i));
      else
          return Polygon_Raise(ERR_IND);
  } else {
      PyObject *OL;
      OL = PyTuple_New(self->p->num_contours);
      for (i = 0; i < self->p->num_contours; i++)
          PyTuple_SetItem(OL, i, PyFloat_FromDouble(poly_c_orientation(self->p->contour+i)));
      return Py_BuildValue("O", OL);
  }
}


#define DOCSTR_POLY_CENTER \
"center(|i)\n\
argument: optional  contour index\n\
returns: a 2-tuple containing x and y float values\n\
Calculates the center of gravity of one contour (when called with index) or of\n\
the whole Polygon. The center may  be outside the contours or inside holes.\n\
This is not the center of the bounding box!"
static PyObject *Polygon_center(Polygon *self, PyObject *args) {
  int i=INDEF;
  double cx, cy;
  if (! PyArg_ParseTuple(args, "|i", &i))
      return Polygon_Raise(ERR_ARG);
  if (i!=INDEF) {
      if ((i >= 0) && (i < self->p->num_contours)) {
          if (poly_c_center(self->p->contour+i, &cx, &cy) !=0)
              return Polygon_Raise(ERR_INV);
      } else
          return Polygon_Raise(ERR_IND);
  } else {
      if (poly_p_center(self->p, &cx, &cy) != 0)
          return Polygon_Raise(ERR_INV);
  }
  return Py_BuildValue("dd", cx, cy);
}


#define DOCSTR_POLY_ASPECTRATIO \
"aspectRatio(|i)\n\
argument: optional contour index\n\
returns: a float\n\
Calculates the ratio delta_y/delta_x of the boundingbox of the polygon."
static PyObject *Polygon_aspectRatio(Polygon *self, PyObject *args) {
  int i=INDEF;
  double x0, x1, y0, y1;
  if (! PyArg_ParseTuple(args, "|i", &i))
      return Polygon_Raise(ERR_ARG);
  if (i!=INDEF) {
      if ((i >= 0) && (i < self->p->num_contours))
          poly_c_boundingbox(self->p->contour+i, &x0, &x1, &y0, &y1);
      else
          return Polygon_Raise(ERR_IND);
  } else
      Polygon_getBoundingBox(self, &x0, &x1, &y0, &y1);
  return Py_BuildValue("d", ((x0 != x1) ? fabs((y1-y0)/(x1-x0)) : 0.0));
}


#define DOCSTR_POLY_BOUNDINGBOX \
"boundingBox(|i)\n\
argument: optional contour index\n\
returns: tuple of four floats: xmin, xmax, ymin and ymax\n\
Calculates the bounding box  of one contour (when called with index) or of the\n\
whole polygon. In the latter case the data is cached and used for following \n\
calls and internal calculations. The data will be recalculated automatically \n\
when this method is called after the polygon has changed."
static PyObject *Polygon_boundingBox(Polygon *self, PyObject *args) {
  int i=INDEF;
  double x0, x1, y0, y1;
  if (! PyArg_ParseTuple(args, "|i", &i))
      return Polygon_Raise(ERR_ARG);
  if (i!=INDEF) {
      if ((i >= 0) && (i < self->p->num_contours))
          poly_c_boundingbox(self->p->contour+i, &x0, &x1, &y0, &y1);
      else
          return Polygon_Raise(ERR_IND);
  } else
      Polygon_getBoundingBox(self, &x0, &x1, &y0, &y1);
  return Py_BuildValue("dddd", x0, x1,y0,y1);
}


#define DOCSTR_POLY_ISHOLE \
"isHole(|i)\n\
argument: optional contour index\n\
returns: an integer (0/1) or a tuple of integers\n\
Returns the hole flag of a single contour (when called with index argument) or\n\
a list of all flags when called without arguments."
static PyObject *Polygon_isHole(Polygon *self, PyObject *args) {
  int i=INDEF;
  if (! PyArg_ParseTuple(args, "|i", &i))
      return Polygon_Raise(ERR_ARG);
  if (i!=INDEF) {
      if ((i >= 0) && (i < self->p->num_contours))  
          return Py_BuildValue("i", (self->p->hole[i] > 0) ? 1 : 0);
      else 
          return Polygon_Raise(ERR_IND);
  } else {
      PyObject *O;
      O = PyTuple_New(self->p->num_contours);
      for (i = 0; i < self->p->num_contours; i++)
          PyTuple_SetItem(O, i, PyInt_FromLong((self->p->hole[i] > 0) ? 1 : 0));
      return Py_BuildValue("O", O);
  }
}


#define DOCSTR_POLY_ISSOLID \
"isSolid(|i)\n\
argument: optional  contour index\n\
returns: an integer (0/1) or a tuple of integers\n\
Returns the inverted hole flag of a single contour (when called with index \n\
argument) or a list  of all inverted flags when called without arguments."
static PyObject *Polygon_isSolid(Polygon *self, PyObject *args) {
  int i=INDEF;
  if (! PyArg_ParseTuple(args, "|i", &i))
      return Polygon_Raise(ERR_ARG);
  if (i!=INDEF) {
      if ((i >= 0) && (i < self->p->num_contours))  
          return Py_BuildValue("i", (self->p->hole[i] > 0) ? 0 : 1);
      else 
          return Polygon_Raise(ERR_IND);
  } else {
      PyObject *O;
      O = PyTuple_New(self->p->num_contours);
      for (i = 0; i < self->p->num_contours; i++)
          PyTuple_SetItem(O, i, PyInt_FromLong((self->p->hole[i] > 0) ? 0 : 1));
      return Py_BuildValue("O", O);
  }
}


#define DOCSTR_POLY_ISINSIDE \
"isInside(x, y |, i)\n\
arguments:\n\
  - two float values:  x and y\n\
  - and an optional contour index\n\
returns: 1 for inside, 0 for outside (or inside a hole)\n\
Point containment test: returns logical  containment value for a single contour\n\
(when called with index) or of  the whole Polygon. If point is exactly on the \n\
border, the value may be 0 or 1, sorry!"
static PyObject *Polygon_isInside(Polygon *self, PyObject *args) {
  int i=INDEF, r=0;
  double x, y;
  if (! PyArg_ParseTuple(args, "dd|i", &x, &y, &i))
      return Polygon_Raise(ERR_ARG);
  if (i!=INDEF) {
      if ((i >= 0) && (i < self->p->num_contours)) {
          if ((r = poly_c_point_inside(self->p->contour+i, x, y)) == -1)
              return Polygon_Raise(ERR_INV);
      } else
          return Polygon_Raise(ERR_IND);
  } else {
      if ((r = poly_p_point_inside(self->p, x, y)) == -1)
          return Polygon_Raise(ERR_INV);
  }
  return Py_BuildValue("i",  r);
}


#define DOCSTR_POLY_COVERS \
"covers(p)\n\
argument: another polygon object\n\
returns: integer (0/1)\n\
Tests if the polygon completely covers the other polygon p. At first bounding \n\
boxes are tested for obvious cases and then an optional clipping is performed."
static PyObject *Polygon_covers(Polygon *self, Polygon *other) {
  double x0, x1, y0, y1, X0, X1, Y0, Y1;
  gpc_polygon * pres;
  int r;
  if (! Polygon_Check(other))
      return Polygon_Raise(ERR_ARG);
  Polygon_getBoundingBox(self,  &x0, &x1, &y0, &y1);
  Polygon_getBoundingBox(other, &X0, &X1, &Y0, &Y1);
  /* first test if bounding box covers other boundingbox */ 
  if ((X0 < x0) || (X1 > x1) || (Y0 < y0) || (Y1 > y1))
      return Py_BuildValue("i",  0);
  /* still there? Let's do the full test... */  
  if (! (pres = poly_p_new())) return Polygon_Raise(ERR_MEM);
  gpc_polygon_clip(GPC_DIFF, other->p, self->p, pres);
  r = pres->num_contours;
  gpc_free_polygon(pres);
  free(pres);
  return Py_BuildValue("i",  ((r > 0) ? 0 : 1));
}


#define DOCSTR_POLY_OVERLAPS \
"overlaps(p)\n\
argument: another polygon object\n\
returns: integer(0/1)\n\
Tests if the polygon overlaps the other polygon p. At first bounding boxes are\n\
tested for obvious cases and then an optional clipping is performed."
static PyObject *Polygon_overlaps(Polygon *self, Polygon *other) {
  double x0, x1, y0, y1, X0, X1, Y0, Y1;
  gpc_polygon * pres;
  int r;
  if (! Polygon_Check(other))
      return Polygon_Raise(ERR_ARG);
  Polygon_getBoundingBox(self,  &x0, &x1, &y0, &y1);
  Polygon_getBoundingBox(other, &X0, &X1, &Y0, &Y1);
  /* first test if bounding box overlaps other boundingbox */ 
  if ((X0 > x1) || (x0 > X1) || (Y0 > y1) || (y0 > Y1))
      return Py_BuildValue("i",  0);
  /* still there? Let's do the full test... */
  if (! (pres = poly_p_new())) return Polygon_Raise(ERR_MEM);
  gpc_polygon_clip(GPC_INT, other->p, self->p, pres);
  r = pres->num_contours;
  gpc_free_polygon(pres);
  free(pres);
  return Py_BuildValue("i",  ((r > 0) ? 1 : 0));
}


#define DOCSTR_POLY_TRISTRIP \
"triStrip()\n\
argument: None\n\
returns: list of TriStrips (point lists)\n\
A TriStrip is a list of triangles. The sum of all triangles fill the TriStrip\n\
area. The triangles usually are not in a good shape for FEM methods!\n\
The object returned by the triStrip()-method represents a list of strips. Each\n\
strip stores triangle data by an efficient method. A strip is a tuple \n\
containing points (2-tuples). The first three items of the tuple belong to the\n\
first triangle. The second, third and fourth item are the corners of the second\n\
triangle. Item number three, four and five are the corners of the third\n\
triangle, (...you may guess the rest!). The example on the right shows an area\n\
which is described by three strips. The number of triangles in a strip is the\n\
number of points lowered by 2."
static PyObject *Polygon_triStrip(Polygon *self) {
    gpc_tristrip *t = (gpc_tristrip *)alloca(sizeof(gpc_tristrip));
    gpc_vertex_list *vl;
    PyObject *R, *TS;
    int i, j;
    t->num_strips = 0;
    t->strip = NULL;
    gpc_polygon_to_tristrip(self->p, t);
    switch (dataStyle) {
        case STYLE_TUPLE: {
            PyObject *P;
            gpc_vertex *v;
            R = PyTuple_New(t->num_strips);
            for (i=0; i < t->num_strips; i++) {
                vl = t->strip + i;
                v = vl->vertex;
                TS = PyTuple_New(vl->num_vertices);
                for (j=0; j < vl->num_vertices; j++) {
                    P = PyTuple_New(2);
                    PyTuple_SetItem(P, 0, PyFloat_FromDouble(v->x));
                    PyTuple_SetItem(P, 1, PyFloat_FromDouble(v->y));
                    PyTuple_SetItem(TS, j, P);
                    v++;
                }
                PyTuple_SetItem(R, i, TS);
            }
        } break;
        case STYLE_LIST: {
            PyObject *P;
            gpc_vertex *v;
            R = PyList_New(t->num_strips);
            for (i=0; i < t->num_strips; i++) {
                vl = t->strip + i;
                v = vl->vertex;
                TS = PyList_New(vl->num_vertices);
                for (j=0; j < vl->num_vertices; j++) {
                    P = PyTuple_New(2);
                    PyTuple_SetItem(P, 0, PyFloat_FromDouble(v->x));
                    PyTuple_SetItem(P, 1, PyFloat_FromDouble(v->y));
                    PyList_SetItem(TS, j, P);
                    v++;
                }
                PyList_SetItem(R, i, TS);
            }
        } break;
#ifdef WITH_NUMERIC
        case STYLE_ARRAY: {
            int dims[2] = {0, 2};
            R = PyTuple_New(t->num_strips);
            for (i=0; i < t->num_strips; i++) {
                vl = t->strip + i;
                dims[0] = vl->num_vertices;
                TS = PyArray_FromDims(2, dims, PyArray_DOUBLE);
                memcpy(((PyArrayObject *)TS)->data, vl->vertex, sizeof(gpc_vertex)*vl->num_vertices);
                PyTuple_SetItem(R, i, (PyObject *)TS);
            }
        } break;
#endif /* WITH_NUMERIC */
        default:
            return Polygon_Raise(PolyError, "Unknown data style");
    }
    gpc_free_tristrip(t);
    return Py_BuildValue("O", R);
}


static PyObject *Polygon_getattr(Polygon *self, char *name) {
    if (self->attr != NULL) {
        PyObject *v = PyDict_GetItemString(self->attr, name);
        if (v != NULL) {
            Py_INCREF(v);
            return v;
        }
    }
    return Py_FindMethod(Polygon_Methods, (PyObject *)self, name);
}


static int Polygon_setattr(Polygon *self, char *name, PyObject *v) {
    if (self->attr == NULL) {
        self->attr = PyDict_New();
        if (self->attr == NULL)
            return -1;
    }
    if (v == NULL) {
        int rv = PyDict_DelItemString(self->attr, name);
        if (rv < 0)
            PyErr_SetString(PyExc_AttributeError,
                            "delete non-existing Polygon attribute");
        return rv;
    }
    else
        return PyDict_SetItemString(self->attr, name, v);
}


static int Polygon_nonzero(PyObject *self) {
    return ((((Polygon *)self)->p->num_contours > 0) ? 1 : 0);
}


static PyObject *Polygon_opDiff(Polygon *self, Polygon *other) {
    gpc_polygon *ret;
    if (! Polygon_Check(other)) return Polygon_Raise(ERR_TYP);
    if (! (ret = poly_p_new())) return Polygon_Raise(ERR_MEM);
    gpc_polygon_clip(GPC_DIFF, self->p, other->p, ret);
    return (PyObject *)Polygon_NEW(ret);
}


static PyObject *Polygon_opUnion(Polygon *self, Polygon *other) {
    gpc_polygon *ret;
    if (! Polygon_Check(other)) return Polygon_Raise(ERR_TYP);
    if (! (ret = poly_p_new())) return Polygon_Raise(ERR_MEM);
    gpc_polygon_clip(GPC_UNION, self->p, other->p, ret);
    return (PyObject *)Polygon_NEW(ret);
}


static PyObject *Polygon_opXor(Polygon *self, Polygon *other) {
    gpc_polygon *ret;
    if (! Polygon_Check(other)) return Polygon_Raise(ERR_TYP);
    if (! (ret = poly_p_new())) return Polygon_Raise(ERR_MEM);
    gpc_polygon_clip(GPC_XOR, self->p, other->p, ret);
    return (PyObject *)Polygon_NEW(ret);
}


static PyObject *Polygon_opInt(Polygon *self, Polygon *other) {
    gpc_polygon *ret;
    if (! Polygon_Check(other)) return Polygon_Raise(ERR_TYP);
    if (! (ret = poly_p_new())) return Polygon_Raise(ERR_MEM);
    gpc_polygon_clip(GPC_INT, self->p, other->p, ret);
    return (PyObject *)Polygon_NEW(ret);
}


static PyNumberMethods Polygon_NumberMethods = {
    (PyCFunction)Polygon_opUnion, /* binaryfunc nb_add;        __add__ */
    (PyCFunction)Polygon_opDiff,  /* binaryfunc nb_subtract;   __sub__ */
    0,               /* binaryfunc nb_multiply;   __mul__ */
    0,               /* binaryfunc nb_divide;     __div__ */
    0,               /* binaryfunc nb_remainder;  __mod__ */
    0,               /* binaryfunc nb_divmod;     __divmod__ */
    0,               /* ternaryfunc nb_power;     __pow__ */
    0,               /* unaryfunc nb_negative;    __neg__ */
    0,               /* unaryfunc nb_positive;    __pos__ */
    0,               /* unaryfunc nb_absolute;    __abs__ */
    Polygon_nonzero, /* inquiry nb_nonzero;       __nonzero__ */
    0,               /* unaryfunc nb_invert;      __invert__ */
    0,               /* binaryfunc nb_lshift;     __lshift__ */
    0,               /* binaryfunc nb_rshift;     __rshift__ */
    (PyCFunction)Polygon_opInt,   /* binaryfunc nb_and;        __and__ */
    (PyCFunction)Polygon_opXor,   /* binaryfunc nb_xor;        __xor__ */
    (PyCFunction)Polygon_opUnion, /* binaryfunc nb_or;         __or__ */
    0,               /* coercion nb_coerce;       __coerce__ */
    0,               /* unaryfunc nb_int;         __int__ */
    0,               /* unaryfunc nb_long;        __long__ */
    0,               /* unaryfunc nb_float;       __float__ */
    0,               /* unaryfunc nb_oct;         __oct__ */
    0,               /* unaryfunc nb_hex;         __hex__ */
};


static PySequenceMethods Polygon_SequenceMethods = {
    Polygon_len,     /* inquiry sq_length;             __len__ */
    0,               /* binaryfunc sq_concat;          __add__ */
    0,               /* intargfunc sq_repeat;          __mul__ */
    Polygon_getitem, /* intargfunc sq_item;            __getitem__ */
    0,               /* intintargfunc sq_slice;        __getslice__ */
    0,               /* intobjargproc sq_ass_item;     __setitem__ */
    0                /* intintobjargproc sq_ass_slice; __setslice__ */
};


static PyMethodDef Polygon_Methods[] = {
  {"addContour",    (PyCFunction)Polygon_addContour,  METH_VARARGS, DOCSTR_POLY_ADDCONTOUR},
  {"contour",       (PyCFunction)Polygon_getContour,  METH_VARARGS, DOCSTR_POLY_CONTOUR},
  {"read",          (PyCFunction)Polygon_read,        METH_VARARGS, DOCSTR_POLY_READ},
  {"write",         (PyCFunction)Polygon_write,       METH_VARARGS, DOCSTR_POLY_WRITE},
  {"simplify",      (PyCFunction)Polygon_simplify,    METH_VARARGS, DOCSTR_POLY_SIMPLIFY},
  {"shift",         (PyCFunction)Polygon_shift,       METH_VARARGS, DOCSTR_POLY_SHIFT},
  {"scale",         (PyCFunction)Polygon_scale,       METH_VARARGS, DOCSTR_POLY_SCALE},
  {"rotate",        (PyCFunction)Polygon_rotate,      METH_VARARGS, DOCSTR_POLY_ROTATE},
  {"warpToBox",     (PyCFunction)Polygon_warpToBox,   METH_VARARGS, DOCSTR_POLY_WARPTOBOX},
  {"flip",          (PyCFunction)Polygon_flip,        METH_VARARGS, DOCSTR_POLY_FLIP},
  {"flop",          (PyCFunction)Polygon_flop,        METH_VARARGS, DOCSTR_POLY_FLOP},
  {"area",          (PyCFunction)Polygon_area,        METH_VARARGS, DOCSTR_POLY_AREA},
  {"orientation",   (PyCFunction)Polygon_orientation, METH_VARARGS, DOCSTR_POLY_ORIENTATION},
  {"center",        (PyCFunction)Polygon_center,      METH_VARARGS, DOCSTR_POLY_CENTER},
  {"boundingBox",   (PyCFunction)Polygon_boundingBox, METH_VARARGS, DOCSTR_POLY_BOUNDINGBOX},
  {"aspectRatio",   (PyCFunction)Polygon_aspectRatio, METH_VARARGS, DOCSTR_POLY_ASPECTRATIO},
  {"isHole",        (PyCFunction)Polygon_isHole,      METH_VARARGS, DOCSTR_POLY_ISHOLE},
  {"isSolid",       (PyCFunction)Polygon_isSolid,     METH_VARARGS, DOCSTR_POLY_ISSOLID},
  {"isInside",      (PyCFunction)Polygon_isInside,    METH_VARARGS, DOCSTR_POLY_ISINSIDE},
  {"covers",        (PyCFunction)Polygon_covers,      METH_O,       DOCSTR_POLY_COVERS},
  {"overlaps",      (PyCFunction)Polygon_overlaps,    METH_O,       DOCSTR_POLY_OVERLAPS},
  {"nPoints",       (PyCFunction)Polygon_nPoints,     METH_VARARGS, DOCSTR_POLY_NPOINTS},
  {"triStrip",      (PyCFunction)Polygon_triStrip,    METH_NOARGS,  DOCSTR_POLY_TRISTRIP},
  {NULL, NULL}, /* sentinel */
};


static PyTypeObject Polygon_Type = {
  PyObject_HEAD_INIT(NULL)
  0,                               /*ob_size*/
  "cPolygon.Polygon",               /*tp_name*/
  sizeof(Polygon),                 /*tp_basicsize*/
  0,                               /*tp_itemsize*/
  /* methods */
  (destructor)Polygon_dealloc,     /*tp_dealloc*/
  0,                               /*tp_print*/
  (getattrfunc)Polygon_getattr,    /*tp_getattr*/
  (setattrfunc)Polygon_setattr,    /*tp_setattr*/
  0,                               /*tp_compare*/
  Polygon_repr,                    /* (reprfunc)tp_repr*/
  &Polygon_NumberMethods,          /*tp_as_number*/
  &Polygon_SequenceMethods,        /*tp_as_sequence*/
  0,                               /*tp_as_mapping*/
  0,                               /*tp_hash*/
  0,                               /*tp_call*/
  0,                               /*tp_str*/
  0,                               /*tp_getattro*/
  0,                               /*tp_setattro*/
  0,                               /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT,              /*tp_flags*/
  DOCSTR_POLY_TYPE,                /*tp_doc*/
  0,                               /*tp_traverse*/
  0,                               /*tp_clear*/
  0,                               /*tp_richcompare*/
  0,                               /*tp_weaklistoffset*/
  0,                               /*tp_iter*/
  0,                               /*tp_iternext*/
  0,                               /*tp_methods*/
  0,                               /*tp_members*/
  0,                               /*tp_getset*/
  0,                               /*tp_base*/
  0,                               /*tp_dict*/
  0,                               /*tp_descr_get*/
  0,                               /*tp_descr_set*/
  0,                               /*tp_dictoffset*/
  0,                               /*tp_init*/
  0,                               /*tp_alloc*/
  0,                               /*tp_new*/
  0,                               /*tp_free*/
  0,                               /*tp_is_gc*/
};


/***************************** Module *******************************/
#define DOCSTR_POLY_DATSTYLE \
"setDataStyle(s)\n\
argument: one of STYLE_TUPLE, STYLE_LIST or STYLE_NUMERIC\n\
returns: None\n\
The data style defines the type of objects returned by some functions.\n\
Point lists may be returned as tuples, lists or Numeric.arrays (of compiled\n\
with support for Numeric)."
static PyObject * setDataStyle(PyObject *self, PyObject *arg) {
    if (! PyInt_Check(arg))
        return Polygon_Raise(ERR_ARG);
    dataStyle = PyInt_AsLong(arg);
    return Py_BuildValue("O",  Py_None);
}

#ifndef CONST_EPSILON
#define DOCSTR_POLY_SETTOLERANCE \
"setTolerance(t)\n\
argument: float value\n\
returns: None\n\
The tolerance is used to test if two points are the same. Increasing\n\
the value will be needed when point coordinates are not accurate\n\
(maybe because of a lot of conversions). Defaults to DBL_EPSILON."
static PyObject * setEpsilon(PyObject *self, PyObject *arg) {
    if (PyFloat_Check(arg))
        GPC_EPSILON = PyFloat_AsDouble(arg);
    else if (PyInt_Check(arg))
        GPC_EPSILON = PyInt_AsLong(arg);
    else if (PyLong_Check(arg))
        GPC_EPSILON = PyLong_AsLong(arg);
    else
        return Polygon_Raise(ERR_ARG);
    return Py_BuildValue("O",  Py_None);
}

#define DOCSTR_POLY_GETTOLERANCE \
"getTolerance()\n\
argument: None\n\
returns: float value\n\
Returns the tolerance value. See setTolerance() for details."
static PyObject * getEpsilon(PyObject *self) {
    return Py_BuildValue("d", GPC_EPSILON);
}
#endif /* CONST_EPSILON */

static PyMethodDef cPolygonMethods[] = {
    {"Polygon",      (PyCFunction)Polygon_new,  METH_VARARGS, DOCSTR_POLY_TYPE},
    {"setDataStyle", (PyCFunction)setDataStyle, METH_O      , DOCSTR_POLY_DATSTYLE},
#ifndef CONST_EPSILON
    {"setTolerance", (PyCFunction)setEpsilon,   METH_O      , DOCSTR_POLY_SETTOLERANCE},
    {"getTolerance", (PyCFunction)getEpsilon,   METH_NOARGS , DOCSTR_POLY_GETTOLERANCE},
#endif /* CONST_EPSILON */
    {NULL,      NULL}        /* Sentinel */
};

DL_EXPORT(void) initcPolygon(void) {
    PyObject *m, *d;
    Polygon_Type.ob_type = &PyType_Type;
    m = Py_InitModule3("cPolygon", cPolygonMethods, DOCSTR_POLY_MODULE);
#ifdef WITH_NUMERIC
    import_array();
#endif /* WITH_NUMERIC */
    d = PyModule_GetDict(m);
    PolyError = PyErr_NewException("cPolygon.Error", NULL, NULL);
    PyDict_SetItemString(d, "Error", PolyError);
    PyDict_SetItemString(d, "PolygonType", (PyObject *)(&Polygon_Type));
    PyDict_SetItemString(d, "STYLE_TUPLE", (PyObject *)PyInt_FromLong(STYLE_TUPLE));
    PyDict_SetItemString(d, "STYLE_LIST", (PyObject *)PyInt_FromLong(STYLE_LIST));
#ifdef WITH_NUMERIC
    PyDict_SetItemString(d, "STYLE_ARRAY", (PyObject *)PyInt_FromLong(STYLE_ARRAY));
    PyDict_SetItemString(d, "withNumeric", (PyObject *)PyInt_FromLong(1));
#else
    PyDict_SetItemString(d, "withNumeric", (PyObject *)PyInt_FromLong(0));
#endif /* WITH_NUMERIC */
    PyDict_SetItemString(d, "version", (PyObject *)PyFloat_FromDouble(POLYVERSION));
    PyDict_SetItemString(d, "__version__", (PyObject *)PyFloat_FromDouble(POLYVERSION));
    PyDict_SetItemString(d, "author", (PyObject *)PyString_FromString(POLY_AUTHOR));
    PyDict_SetItemString(d, "__author__", (PyObject *)PyString_FromString(POLY_AUTHOR));
    PyDict_SetItemString(d, "license", (PyObject *)PyString_FromString(POLY_LICENSE));
    PyDict_SetItemString(d, "__license__", (PyObject *)PyString_FromString(POLY_LICENSE));
}
