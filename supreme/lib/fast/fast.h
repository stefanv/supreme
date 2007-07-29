#ifndef FAST_H
#define FAST_H

typedef struct { int x, y; } xy;
typedef unsigned char byte;

xy*  fast_nonmax(const byte* im, int xsize, int ysize, xy* corners, int numcorners, int barrier, int* numnx);
xy*  fast_corner_detect_9(const byte* im, int xsize, int ysize, int barrier, int* numcorners);
xy*  fast_corner_detect_10(const byte* im, int xsize, int ysize, int barrier, int* numcorners);
xy*  fast_corner_detect_11(const byte* im, int xsize, int ysize, int barrier, int* numcorners);
xy*  fast_corner_detect_12(const byte* im, int xsize, int ysize, int barrier, int* numcorners);

/* Added this to make sure allocation and deallocation */
/* takes place in the same library */
void fast_free(xy* ptr);

#endif
