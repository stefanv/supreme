/* Point of intersection */
struct POI {
    double x, y;
    int type; /* 0 -- ordinary
                 1 -- intersects outside start and end-points
                 2 -- parallel
                 3 -- co-incident
                 */
};

unsigned char pnpoly(int nr_verts, double *xp, double *yp, double x, double y);
void npnpoly(int nr_verts, double *xp, double *yp,
             int N, double *x, double *y,
             unsigned char *result);
void line_intersect(double x0, double y0, double x1, double y1, /* line 1 */
                    double x2, double y2, double x3, double y3, /* line 2 */
                    struct POI *p);
int poly_clip(int N, double* x, double* y,
              double xleft, double xright, double ytop, double ybottom,
              double* workx, double* worky);
void tf_polygon(int N, double* xp, double* yp, double* tf_M);
double area(int N, double* px, double* py);
void interp_transf_polygon(int target_rows, int target_cols,
                           unsigned char* target,
                           int out_rows, int out_cols, double* out,
                           double* inv_tf_M);
