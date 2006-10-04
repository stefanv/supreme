/* Code from:
   http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

   Copyright (c) 1970-2003, Wm. Randolph Franklin

   Copyright (c) 2006, Stefan van der Walt

   Permission is hereby granted, free of charge, to any person
   obtaining a copy of this software and associated documentation
   files (the "Software"), to deal in the Software without
   restriction, including without limitation the rights to use, copy,
   modify, merge, publish, distribute, sublicense, and/or sell copies
   of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

    1. Redistributions of source code must retain the above
         copyright notice, this list of conditions and the following
         disclaimers.
    2. Redistributions in binary form must reproduce the above
         copyright notice in the documentation and/or other materials
         provided with the distribution.
    3. The name of W. Randolph Franklin may not be used to endorse
         or promote products derived from this Software without
         specific prior written permission. 

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
   BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
   ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
   CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE. */

#ifdef __cplusplus
extern "C" {
#endif

int pnpoly(int nr_verts, double *xp, double *yp, double x, double y)
{
    int i,j, c=0;
    for (i = 0, j = nr_verts-1; i < nr_verts; j = i++) {
        if ((((yp[i]<=y) && (y<yp[j])) ||
             ((yp[j]<=y) && (y<yp[i]))) &&
            (x < (xp[j] - xp[i]) * (y - yp[i]) / (yp[j] - yp[i]) + xp[i]))
	    
	    c = !c;
    }
    return c;
}

void npnpoly(int nr_verts, double *xp, double *yp,
	     int nr_points, double *x, double *y,
	     int *result)
/*
 * For N provided points, calculate whether they are in
 * the polygon defined by vertices *xp, *yp.
 *
 * nr_verts : number of vertices
 * *xp, *yp : x and y coordinates of vertices
 * nr_points : number of data points provided
 * *x, *y : data points
 */
{
    int n = 0;
    for (n = 0; n < nr_points; n++) {
	result[n] = pnpoly(nr_verts,xp,yp,x[n],y[n]);
    }
}

/* Point of intersection */
struct POI {
    double x, y;
    int type; /* 0 -- ordinary
		 1 -- intersects outside start and end-points 
                 2 -- parallel
                 3 -- co-incident 
	         */
};

void line_intersect(double x0, double y0, double x1, double y1, /* line 1 */
		    double x2, double y2, double x3, double y3, /* line 2 */
		    struct POI *p)
/*
  Calculate the point of intersection between two lines.
 */
{
    double d, ua, ub;

    d = (y3 - y2)*(x1 - x0) - (x3 - x2)*(y1 - y0);
    ua = (x3 - x2)*(y0 - y2) - (y3 - y2)*(x0 - x2);
    ub = (x1 - x0)*(y0 - y2) - (y1 - y0)*(x0 - x2);

    if (d == 0) {
	p->x = 0;
	p->y = 0;

	if ((ua == 0) && (ub == 0))
	    p->type = 3;
	else
	    p->type = 2;
	return;
    }

    ua = ua/d;
    ub = ub/d;

    p->x = x0 + ua*(x1 - x0); 
    p->y = y0 + ua*(y1 - y0); 
    if ((ua >= 0) && (ua <= 1) && (ub >= 0) && (ub <= 1))
	p->type = 0;
    else
	p->type = 1;

    return;
}

#ifdef __cplusplus
}
#endif
