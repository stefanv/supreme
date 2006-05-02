/*      $Id: PolyUtil.c,v 1.8 2004/10/26 15:10:32 joerg Exp $    */
#include "PolyUtil.h"
#include <math.h>
#include <string.h>
#include <stdlib.h>

#ifdef SYSTEM_WIN32
#include <malloc.h>
#endif /*SYSTEM_WIN32*/


gpc_polygon * poly_p_new() {
  gpc_polygon *p = (gpc_polygon *)malloc(sizeof(gpc_polygon));
  if (p) {
      p->num_contours = 0;
      p->contour = NULL;
      p->hole = NULL;
  }
  return p;
}


int poly_p_clone(gpc_polygon *s, gpc_polygon *t) {
    gpc_vertex_list *svl, *tvl;
    int i;
    /* may be done much faster with copying whole memory areas? */
    t->num_contours = s->num_contours;
    t->contour = (gpc_vertex_list *)malloc(sizeof(gpc_vertex_list) * t->num_contours);
    t->hole = (int *)malloc(sizeof(int)*t->num_contours);
    if ((! t->contour) || (! t->hole)) return -1;
    for (i=0; i < t->num_contours; i++) {
        t->hole[i] = s->hole[i];
        svl = s->contour + i;
        tvl = t->contour + i;
        tvl->num_vertices = svl->num_vertices;
        if (! (tvl->vertex = (gpc_vertex *)malloc(sizeof(gpc_vertex) * tvl->num_vertices)))
            return -1;
        memcpy(tvl->vertex, svl->vertex, sizeof(gpc_vertex) * svl->num_vertices);
    }
    return 0;
}


double poly_c_area(gpc_vertex_list *vl) {
  int i;
  double a = 0.0;
  for (i=0; i < vl->num_vertices-1; i++)
      a += ((vl->vertex[i].x + vl->vertex[i+1].x) *
            (vl->vertex[i+1].y - vl->vertex[i].y));
  /* close the loop */
  a += ((vl->vertex[i].x + vl->vertex->x) *
        (vl->vertex->y - vl->vertex[i].y));
  return 0.5*fabs(a);
}


double poly_p_area(gpc_polygon *p) {
  int i;
  double a = 0.0;
  for (i = 0; i < p->num_contours; i++)
    a += ((p->hole[i]) ? -1.0 : 1.0) * poly_c_area(p->contour+i);
  return a;
}


int poly_c_orientation(gpc_vertex_list *vl) {
  /* return 1 for cw, -1 for ccw) */
  gpc_vertex *v, *a, *b, *c;
  int i, m;
  double area;
  /* find lowest rightmost vertex */
  v = b = vl->vertex;
  m = 0;
  for (i=0; i < vl->num_vertices; i++) {
    v = vl->vertex + i;
    if ((v->y < b->y) || ((v->y == b->y) && (v->x > b->x))) {
      m = i; b = v;
    }
  }
  /* now m is the lowest rightmost vertex, find orientation */
  a = vl->vertex + ((m + (vl->num_vertices-1)) % vl->num_vertices);
  c = vl->vertex + ((m+1) % vl->num_vertices);
  area = (a->x*b->y - a->y*b->x + a->y*c->x - a->x*c->y + 
          b->x*c->y - c->x*b->y);
  if (area > 0)
    return 1;
  else if (area < 0)
    return -1;
  else
    return 0;
}


int poly_c_center(gpc_vertex_list *vl, double *cx, double *cy){
  gpc_vertex *v;
  double x=0.0, y=0.0, a;
  int i;
  for (i=0; i < vl->num_vertices-1; i++) {
    v = vl->vertex + i;
    a = v->x * (v+1)->y - (v+1)->x * v->y;
    x += (v->x + (v+1)->x) * a;
    y += (v->y + (v+1)->y) * a;
  }
  /* close the loop */
  v = vl->vertex + (vl->num_vertices-1);
  a = v->x * vl->vertex->y - vl->vertex->x * v->y;
  x += (v->x + vl->vertex->x) * a;
  y += (v->y + vl->vertex->y) * a;
  /* this algorithm needs ccw ordered points,
     so we have to calculate the order and multiply,
     what a waste of cpu power... 
     If you know a better way, let me know... */
  a = 6.0*poly_c_area(vl)*poly_c_orientation(vl);
  if (a == 0)
      return 1;
  *cx = x / a;
  *cy = y / a;
  return 0;
}


int poly_p_center(gpc_polygon *p, double *cx, double *cy){
  double *x, *y, *a, A=0.0, X=0.0, Y=0.0;
  int i;
  size_t s;
  s = sizeof(double)*p->num_contours;
  a =  (double *)alloca(s);
  x = (double *)alloca(s);
  y = (double *)alloca(s);
  for (i=0; i < p->num_contours; i++) {
    a[i] = ((p->hole[i]) ? -1.0 : 1.0) * poly_c_area(p->contour+i);
    if (poly_c_center(p->contour+i, x+i, y+i) != 0)
        return 1;
  }
  for (i=0; i < p->num_contours; i++)
    A += a[i];
  for (i=0; i < p->num_contours; i++) {
    X += a[i] * x[i];
    Y += a[i] * y[i];
  }
  if (A == 0)
      return 1;
  *cx = X / A;
  *cy = Y / A;
  return 0;
}


int poly_c_point_inside(gpc_vertex_list *vl, double x, double y){
  int i, j, c=0;
  gpc_vertex *vi, *vj;
  for (i=0, j=vl->num_vertices-1; i < vl->num_vertices; j = i++) {
      vi = vl->vertex+i;
      vj = vl->vertex+j;
      if ((((vi->y <= y) && (y < vj->y)) || ((vj->y <= y) && (y < vi->y))))
          if ((x < (vj->x - vi->x) * (y - vi->y) / (vj->y - vi->y) + vi->x))
              c = !c;
  }
  return c;
}


int poly_p_point_inside(gpc_polygon *p, double x, double y){
  int i, inSolid = 0, inHole = 0;
  for(i=0; i< p->num_contours; i++) {
      /* loop over solid contours */
      if (p->hole[i] == 0) {
          inSolid = poly_c_point_inside(p->contour + i, x, y);
          if (inSolid == -1)
              return inSolid; /* error */
          if (inSolid > 0)
              break;
      }
  }
  if (inSolid == 0) 
      return 0;
  for(i=0; i < p->num_contours; i++) {
      /* loop over holes */
      if (p->hole[i] == 1) {
          inHole = poly_c_point_inside(p->contour + i, x, y);
          if (inHole == -1)
              return inHole; /* error */
          if (inHole > 0) 
              break;
      }
  }
  return ((inHole > 0) ? 0 : 1);
}


void poly_c_boundingbox(gpc_vertex_list *vl, double *x0, double *x1, 
                   double *y0, double *y1) {
    int i;
    gpc_vertex *v;
    v = vl->vertex;
    *x0 = *x1 = v->x;
    *y0 = *y1 = v->y;
    for (i=1; i < vl->num_vertices; i++) {
        v = vl->vertex + i;
        if (v->x < *x0) *x0 = v->x;
        if (v->x > *x1) *x1 = v->x;
        if (v->y < *y0) *y0 = v->y;
        if (v->y > *y1) *y1 = v->y;
    }
}


void poly_p_boundingbox(gpc_polygon *p, double *x0, double *x1, 
                   double *y0, double *y1) {
  int i;
  double X0, X1, Y0, Y1; 
  if (p->num_contours <= 0) {
    *x0 = *x1 = *y0 = *y1 = 0.0;
    return;
  }
  poly_c_boundingbox(p->contour, x0, x1, y0, y1);
  for (i=1; i < p->num_contours; i++) {
    poly_c_boundingbox(p->contour+i, &X0, &X1, &Y0, &Y1);
    if (X0 < *x0) *x0 = X0;
    if (X1 > *x1) *x1 = X1;
    if (Y0 < *y0) *y0 = Y0;
    if (Y1 > *y1) *y1 = Y1;
  }
}


void poly_p_shift(gpc_polygon *p, double x, double y) {
  int i, j;
  gpc_vertex_list *vl;
  for (i=0; i < p->num_contours; i++) {
    vl = p->contour+i;
    for (j=0; j < vl->num_vertices; j++) {
      vl->vertex[j].x += x;
      vl->vertex[j].y += y;
    }
  }
}


void poly_p_scale(gpc_polygon *p, double xs, double ys, 
             double xc, double yc) {
  int i, j;
  gpc_vertex_list *vl;
  for (i=0; i < p->num_contours; i++) {
    vl = p->contour+i;
    for (j=0; j < vl->num_vertices; j++) {
      vl->vertex[j].x = xc + xs * (vl->vertex[j].x - xc);
      vl->vertex[j].y = yc + ys * (vl->vertex[j].y - yc);
    }
  }
}


void poly_p_rotate(gpc_polygon *p, double alpha, 
              double xc, double yc) {
  int i, j;
  double x, y, l, a;
  gpc_vertex_list *vl;
  for (i=0; i < p->num_contours; i++) {
    vl = p->contour+i;
    for (j=0; j < vl->num_vertices; j++) {
      x = vl->vertex[j].x - xc;
      y = vl->vertex[j].y - yc;
      l = sqrt(x*x + y*y);
      a = alpha + ((l != 0.0) ? acos(x/l) * 
                   ((y>0.0) ? 1.0 : -1.0) : 0.0);
      vl->vertex[j].x = xc + l * cos(a);
      vl->vertex[j].y = yc + l * sin(a);
    }
  }
}


void poly_p_warpToBox(gpc_polygon *p, double x0, double x1, 
                 double y0, double y1, double *bb) {
  int i, j;
  gpc_vertex_list *vl;
  double xscale, yscale, bx0, bx1, by0, by1;
  if (bb) {
      bx0 = bb[0];
      bx1 = bb[1];
      by0 = bb[2];
      by1 = bb[3];
  } else
      poly_p_boundingbox(p, &bx0, &bx1, &by0, &by1);
  xscale = ((bx1 > bx0) ? (x1-x0)/(bx1-bx0) : 1.0); 
  yscale = ((by1 > by0) ? (y1-y0)/(by1-by0) : 1.0);
  for (i=0; i < p->num_contours; i++) {
    vl = p->contour+i;
    for (j=0; j < vl->num_vertices; j++) {
      vl->vertex[j].x = x0 + xscale*(vl->vertex[j].x - bx0);
      vl->vertex[j].y = y0 + yscale*(vl->vertex[j].y - by0);
    }
  }
}


void poly_p_flip(gpc_polygon *p, double x) {
  int i, j;
  double x2 = 2.0 * x;
  gpc_vertex_list *vl;
  for (i=0; i < p->num_contours; i++) {
    vl = p->contour+i;
    for (j=0; j < vl->num_vertices; j++) {
      vl->vertex[j].x = x2 - vl->vertex[j].x;
    }
  }
}


void poly_p_flop(gpc_polygon *p, double y) {
  int i, j;
  double y2 = 2.0 * y;
  gpc_vertex_list *vl;
  for (i=0; i < p->num_contours; i++) {
    vl = p->contour+i;
    for (j=0; j < vl->num_vertices; j++) {
      vl->vertex[j].y = y2 - vl->vertex[j].y;
    }
  }
}


