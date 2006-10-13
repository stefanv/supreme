#ifdef __cplusplus
extern "C" {
#endif

#include <math.h>

void interp_bilinear(int rows, int columns, unsigned char* img,
		     int tf_rows, int tf_columns, double* coord_r, double* coord_c,
		     char mode, unsigned char cval, unsigned char *out)
{
    int tfr, tfc, r_int, c_int, y0, y1, y2, y3;
    double r,c,t,u;
    for (tfr = 0; tfr < tf_rows; tfr++) {
	for (tfc = 0; tfc < tf_columns; tfc++) {
	    r = coord_r[tfr*tf_columns + tfc];
	    c = coord_c[tfr*tf_columns + tfc];

	    if ((mode == 'N') && ((r < 0) || (r >= rows) ||
				  (c < 0) || (c >= columns)))
		    out[tfr*tf_columns + tfc] = cval;
	    else {
		switch (mode) {
		case 'M': /* mirror */		    
		    if (r < 0) r = fmod(-r,rows);
		    if (c < 0) c = fmod(-c,columns);
		    if (r >= rows) r = rows - fmod(r,rows);
		    if (c >= columns) c = columns - fmod(c,rows);
		    break;
		case 'W': /* wrap */
		    if (r < 0) r = rows - fmod(-r,rows);
		    if (c < 0) c = rows - fmod(-c,columns);
		    if (r >= rows) r = fmod(r,rows);
		    if (c >= columns) c = fmod(c,columns);
		    break;
		}

		r_int = floor(r);
		c_int = floor(c);

		t = r - r_int;
		u = c - c_int;
	    
		/* this is not correct, but the artifacts are small enough that
                   we can ignore it for now (should call coordinate wrapper again) */
		y0 = img[(r_int % rows)*columns + (c_int % columns)];
		y1 = img[((r_int+1) % rows)*columns + ((c_int) % columns)];
		y2 = img[((r_int+1) % rows)*columns + ((c_int+1) % columns)];
		y3 = img[(r_int % rows)*columns + ((c_int+1) % columns)];
		
		out[tfr*tf_columns + tfc] = \
		    (1-t)*(1-u)*y0 + t*(1-u)*y1 + t*u*y2 + (1-t)*u*y3;
	    }
	}
    }
}

#ifdef __cplusplus
}
#endif
