#ifdef __cplusplus
extern "C" {
#endif

#include <math.h>

double coord_map(int* dim, double coord, char* mode) {
    switch (*mode) {
    case 'M': /* mirror */
        if (coord < 0) coord = fmod(-coord,*dim);
        if (coord == *dim) coord = *dim-1;
        if (coord > *dim) coord = *dim - fmod(coord,*dim);
        break;
    case 'W': /* wrap */
        if (coord < 0) coord = *dim - fmod(-coord,*dim);
        if (coord == *dim) coord = 0;
        if (coord > *dim) coord = fmod(coord,*dim);
        break;
    }
    return coord;
}

void interp_bilinear(int rows, int columns, unsigned char* img,
                     int tf_rows, int tf_columns, double* coord_r, double* coord_c,
                     char mode, unsigned char cval, unsigned char *out)
{
    int tfr, tfc, y0, y1, y2, y3;
    double r,c,t,u,r_int,c_int,C;
    C = (double)cval;
    for (tfr = 0; tfr < tf_rows; tfr++) {
        for (tfc = 0; tfc < tf_columns; tfc++) {
            r = coord_r[tfr*tf_columns + tfc];
            c = coord_c[tfr*tf_columns + tfc];

            if ((mode == 'C') && ((r < 0) || (r >= rows) ||
                                  (c < 0) || (c >= columns)))
                out[tfr*tf_columns + tfc] = cval;
            else {
                r = coord_map(&rows,r,&mode);
                c = coord_map(&columns,c,&mode);

                r_int = floor(r);
                c_int = floor(c);

                t = r - r_int;
                u = c - c_int;

                y0 = img[(int)(r_int*columns + c_int)];
                y1 = img[(int)(coord_map(&rows,r_int+1,&mode)*columns + c_int)];
                y2 = img[(int)(coord_map(&rows,r_int+1,&mode)*columns +
                               coord_map(&columns,c_int+1,&mode))];
                y3 = img[(int)(r_int*columns +
                               coord_map(&columns,c_int+1,&mode))];

                out[tfr*tf_columns + tfc] =                             \
                    (1-t)*(1-u)*y0 + t*(1-u)*y1 + t*u*y2 + (1-t)*u*y3;
            }
        }
    }
}

#ifdef __cplusplus
}
#endif
