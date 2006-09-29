void variance_map(double* input, int rows, int columns, double* output)
{
    unsigned int r, c, j;
    for (r = 0; r < rows; r++) {
	for (c = 0; c < columns; c++) {
	    j = r*columns + c;
	    output[j] = input[j];
	}
    }
}
