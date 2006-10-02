#ifdef __cplusplus
extern "C" {
#endif

#import <math.h>

void variance_map(int rows, int columns,
		  double* input, double* output,
		  int window_size_rows, int window_size_columns)
{
    unsigned int offset_rows, offset_columns;
    unsigned int r, c, j, k, rr, cc, N;
    double mean, var;

    offset_rows = ceil((window_size_rows-1)/2);
    offset_columns = ceil((window_size_columns-1)/2);
    N = window_size_columns * window_size_rows;

    for (r = 0; r < rows; r++) {
	for (c = 0; c < columns; c++) {
	    j = r*columns + c;

	    mean = 0;
	    var = 0;

	    if ((r >= offset_rows) && (r < rows - offset_rows) &&
		(c >= offset_columns) && (c < columns - offset_columns)) {

		// Calculate mean
		for (rr = 0; rr < window_size_rows; rr++)
		    for (cc = 0; cc < window_size_columns; cc++) {
			k = (r + rr - offset_rows)*columns + (c + cc - offset_columns);
			mean += input[k];
		    }
		mean = mean / N;
	 
		// Calculate variance
		for (rr = 0; rr < window_size_rows; rr++)
		    for (cc = 0; cc < window_size_columns; cc++) {
			k = (r + rr - offset_rows)*columns + (c + cc - offset_columns);
			var += pow(input[k] - mean, 2);
		    }
		var = var / N;

		output[j] = var;
	    } else {
		output[j] = 0;
	    }
	}
    }
}

#ifdef __cplusplus
extern "C" {
#endif
