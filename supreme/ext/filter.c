void variance_map(int rows, int columns, double* input, double* output)
{
    unsigned int r, c, j;
    for (r = 0; r < rows; r++) {
	for (c = 0; c < columns; c++) {
	    j = r*columns + c;
	    output[j] = input[j];
	}
    }
}
