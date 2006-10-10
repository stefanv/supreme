#ifdef __cplusplus
extern "C" {
#endif

void correlate(int rows_A, int cols_a, double* A,
	       int rows_B, int cols_b, double* B,
	       int steps_row, int steps_col,
	       int mode_row, int mode_col,
	       double* output)
/* Correlate A en B.  Instead of performing the whole correlation,
   only steps_col shifts are done in the x-direction and steps-rows in
   the y-direction.  The mode arguments determine the pixel values
   outside the borders, and can be 0 for 0-value or 1 for
   wrap-around.
   */
{
    int i,j,B_r,B_c,A_r,A_c;
    double val;
    
    /* For all steps */
    for (i = 0; i < steps_col; i++) {
	for (j = 0; j < steps_row; j++) {
	    /* For all pixels in B*/
	    val = 0;
	    for (B_c = 0; B_c < cols_b; B_c++) {
		for (B_r = 0; B_r < rows_B; B_r++) {
		    A_c = B_c + i;
		    A_r = B_r + j;

		    if ((A_c >= cols_a) && (mode_col == 1))
			A_c = A_c % cols_a;
		    if ((A_r >= rows_A) && (mode_row == 1))
			A_r = A_r % rows_A;

		    if ((A_c < cols_a) && (A_r < rows_A)) {
			val += B[B_r*cols_b + B_c] * A[A_r*cols_a + A_c];
		    }
		}
	    }
	    output[j*steps_col + i] = val;
	}
    }
}

#ifdef __cplusplus
}
#endif
