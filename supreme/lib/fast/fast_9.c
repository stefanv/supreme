/* Automatically generated code
force_first_question=0 
corner_pointers=2
*/
#include <stdlib.h>																			
#include "fast.h"																			
xy* fast_corner_detect_9(const byte* im, int xsize, int ysize, int barrier, int* num)				
{																								
	int boundary = 3, y, cb, c_b;																
	const byte  *line_max, *line_min;															
	int			rsize=512, total=0;																
	xy	 		*ret = (xy*)malloc(rsize*sizeof(xy));											
	const byte* cache_0;
	const byte* cache_1;
	const byte* cache_2;
	int	pixel[16];																				
	pixel[0] = 0 + 3 * xsize;		
	pixel[1] = 1 + 3 * xsize;		
	pixel[2] = 2 + 2 * xsize;		
	pixel[3] = 3 + 1 * xsize;		
	pixel[4] = 3 + 0 * xsize;		
	pixel[5] = 3 + -1 * xsize;		
	pixel[6] = 2 + -2 * xsize;		
	pixel[7] = 1 + -3 * xsize;		
	pixel[8] = 0 + -3 * xsize;		
	pixel[9] = -1 + -3 * xsize;		
	pixel[10] = -2 + -2 * xsize;		
	pixel[11] = -3 + -1 * xsize;		
	pixel[12] = -3 + 0 * xsize;		
	pixel[13] = -3 + 1 * xsize;		
	pixel[14] = -2 + 2 * xsize;		
	pixel[15] = -1 + 3 * xsize;		
	for(y = boundary ; y < ysize - boundary; y++)												
	{																							
		cache_0 = im + boundary + y*xsize;														
		line_min = cache_0 - boundary;															
		line_max = im + xsize - boundary + y * xsize;											
																								
		cache_1 = cache_0 + pixel[5];
		cache_2 = cache_0 + pixel[14];
																								
		for(; cache_0 < line_max;cache_0++, cache_1++, cache_2++)
		{																						
			cb = *cache_0 + barrier;															
			c_b = *cache_0 - barrier;															
            if(*cache_1 > cb)
                if(*cache_2 > cb)
                    if(*(cache_0+3) > cb)
                        if(*(cache_0 + pixel[0]) > cb)
                            if(*(cache_0 + pixel[3]) > cb)
                                if(*(cache_0 + pixel[6]) > cb)
                                    if(*(cache_2+4) > cb)
                                        if(*(cache_0 + pixel[15]) > cb)
                                            if(*(cache_0 + pixel[1]) > cb)
                                                goto success;
                                            else if(*(cache_0 + pixel[1]) < c_b)
                                                continue;
                                            else
                                                if(*(cache_0 + pixel[10]) > cb)
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        if(*(cache_0 + pixel[7]) > cb)
                                                            if(*(cache_0 + pixel[9]) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else if(*(cache_0 + pixel[15]) < c_b)
                                            continue;
                                        else
                                            if(*(cache_0 + pixel[8]) > cb)
                                                if(*(cache_0 + pixel[7]) > cb)
                                                    if(*(cache_0 + pixel[1]) > cb)
                                                        goto success;
                                                    else if(*(cache_0 + pixel[1]) < c_b)
                                                        continue;
                                                    else
                                                        if(*(cache_0 + pixel[10]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else if(*(cache_2+4) < c_b)
                                        continue;
                                    else
                                        if(*(cache_1+-6) > cb)
                                            if(*(cache_0 + pixel[9]) > cb)
                                                if(*(cache_0 + pixel[10]) > cb)
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        if(*(cache_0 + pixel[7]) > cb)
                                                            goto success;
                                                        else if(*(cache_0 + pixel[7]) < c_b)
                                                            continue;
                                                        else
                                                            if(*(cache_0+-3) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                    else if(*(cache_0 + pixel[8]) < c_b)
                                                        continue;
                                                    else
                                                        if(*(cache_0+-3) > cb)
                                                            if(*(cache_0 + pixel[1]) > cb)
                                                                if(*(cache_0 + pixel[13]) > cb)
                                                                    goto success;
                                                                else
                                                                    continue;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else if(*(cache_0 + pixel[6]) < c_b)
                                    if(*(cache_0 + pixel[13]) > cb)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            if(*(cache_1+-6) > cb)
                                                continue;
                                            else if(*(cache_1+-6) < c_b)
                                                if(*(cache_0 + pixel[15]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0 + pixel[13]) > cb)
                                        if(*(cache_0 + pixel[15]) > cb)
                                            if(*(cache_2+4) > cb)
                                                if(*(cache_0 + pixel[1]) > cb)
                                                    goto success;
                                                else if(*(cache_0 + pixel[1]) < c_b)
                                                    continue;
                                                else
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        if(*(cache_1+-6) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                            else if(*(cache_2+4) < c_b)
                                                continue;
                                            else
                                                if(*(cache_0 + pixel[9]) > cb)
                                                    if(*(cache_0+-3) > cb)
                                                        if(*(cache_0 + pixel[1]) > cb)
                                                            if(*(cache_0 + pixel[10]) > cb)
                                                                if(*(cache_1+-6) > cb)
                                                                    goto success;
                                                                else
                                                                    continue;
                                                            else
                                                                continue;
                                                        else if(*(cache_0 + pixel[1]) < c_b)
                                                            continue;
                                                        else
                                                            if(*(cache_0 + pixel[8]) > cb)
                                                                if(*(cache_0 + pixel[10]) > cb)
                                                                    goto success;
                                                                else
                                                                    continue;
                                                            else
                                                                continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else if(*(cache_0 + pixel[3]) < c_b)
                                continue;
                            else
                                if(*(cache_0+-3) > cb)
                                    if(*(cache_0 + pixel[10]) > cb)
                                        if(*(cache_1+-6) > cb)
                                            if(*(cache_0 + pixel[8]) > cb)
                                                if(*(cache_0 + pixel[9]) > cb)
                                                    goto success;
                                                else if(*(cache_0 + pixel[9]) < c_b)
                                                    continue;
                                                else
                                                    if(*(cache_2+4) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                            else if(*(cache_0 + pixel[8]) < c_b)
                                                if(*(cache_0 + pixel[7]) > cb || *(cache_0 + pixel[7]) < c_b)
                                                    continue;
                                                else
                                                    goto success;
                                            else
                                                if(*(cache_2+4) > cb)
                                                    if(*(cache_0 + pixel[13]) > cb)
                                                        if(*(cache_0 + pixel[15]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else if(*(cache_2+4) < c_b)
                                                    continue;
                                                else
                                                    if(*(cache_0 + pixel[9]) > cb)
                                                        if(*(cache_0 + pixel[1]) > cb)
                                                            if(*(cache_0 + pixel[13]) > cb)
                                                                if(*(cache_0 + pixel[15]) > cb)
                                                                    goto success;
                                                                else
                                                                    continue;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                        else if(*(cache_0 + pixel[0]) < c_b)
                            if(*(cache_0 + pixel[7]) > cb)
                                if(*(cache_0 + pixel[10]) > cb)
                                    goto success;
                                else
                                    continue;
                            else
                                continue;
                        else
                            if(*(cache_0 + pixel[7]) > cb)
                                if(*(cache_0 + pixel[10]) > cb)
                                    if(*(cache_0 + pixel[3]) > cb)
                                        if(*(cache_0 + pixel[6]) > cb)
                                            if(*(cache_0 + pixel[8]) > cb)
                                                if(*(cache_2+4) > cb)
                                                    if(*(cache_0 + pixel[9]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else if(*(cache_2+4) < c_b)
                                                    continue;
                                                else
                                                    if(*(cache_1+-6) > cb)
                                                        if(*(cache_0 + pixel[9]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                            else
                                                continue;
                                        else if(*(cache_0 + pixel[6]) < c_b)
                                            continue;
                                        else
                                            if(*(cache_0 + pixel[15]) > cb)
                                                if(*(cache_0+-3) > cb)
                                                    if(*(cache_0 + pixel[9]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else if(*(cache_0 + pixel[3]) < c_b)
                                        continue;
                                    else
                                        if(*(cache_0+-3) > cb)
                                            if(*(cache_0 + pixel[8]) > cb)
                                                if(*(cache_1+-6) > cb)
                                                    if(*(cache_0 + pixel[6]) > cb)
                                                        if(*(cache_0 + pixel[9]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else if(*(cache_0 + pixel[6]) < c_b)
                                                        continue;
                                                    else
                                                        if(*(cache_0 + pixel[15]) > cb)
                                                            if(*(cache_0 + pixel[13]) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else if(*(cache_0 + pixel[10]) < c_b)
                                    continue;
                                else
                                    if(*(cache_0 + pixel[1]) > cb)
                                        if(*(cache_0 + pixel[9]) > cb)
                                            if(*(cache_0 + pixel[6]) > cb)
                                                if(*(cache_2+4) > cb)
                                                    if(*(cache_0 + pixel[3]) > cb)
                                                        if(*(cache_0 + pixel[8]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                continue;
                    else if(*(cache_0+3) < c_b)
                        if(*(cache_0+-3) > cb)
                            if(*(cache_0 + pixel[9]) > cb)
                                if(*(cache_1+-6) > cb)
                                    if(*(cache_0 + pixel[10]) > cb)
                                        if(*(cache_0 + pixel[6]) > cb)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                continue;
                        else
                            continue;
                    else
                        if(*(cache_0+-3) > cb)
                            if(*(cache_1+-6) > cb)
                                if(*(cache_0 + pixel[7]) > cb)
                                    if(*(cache_0 + pixel[13]) > cb)
                                        if(*(cache_0 + pixel[10]) > cb)
                                            if(*(cache_0 + pixel[9]) > cb)
                                                if(*(cache_0 + pixel[6]) > cb)
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        goto success;
                                                    else if(*(cache_0 + pixel[8]) < c_b)
                                                        continue;
                                                    else
                                                        if(*(cache_0 + pixel[0]) > cb)
                                                            if(*(cache_0 + pixel[1]) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                else if(*(cache_0 + pixel[6]) < c_b)
                                                    continue;
                                                else
                                                    if(*(cache_0 + pixel[15]) > cb)
                                                        if(*(cache_0 + pixel[8]) > cb)
                                                            goto success;
                                                        else if(*(cache_0 + pixel[8]) < c_b)
                                                            continue;
                                                        else
                                                            if(*(cache_0 + pixel[0]) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                    else
                                                        continue;
                                            else if(*(cache_0 + pixel[9]) < c_b)
                                                continue;
                                            else
                                                if(*(cache_2+4) > cb)
                                                    if(*(cache_0 + pixel[0]) > cb)
                                                        if(*(cache_0 + pixel[1]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else if(*(cache_0 + pixel[10]) < c_b)
                                            continue;
                                        else
                                            if(*(cache_0 + pixel[3]) > cb)
                                                if(*(cache_0 + pixel[1]) > cb)
                                                    if(*(cache_0 + pixel[15]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        continue;
                                else if(*(cache_0 + pixel[7]) < c_b)
                                    if(*(cache_0 + pixel[10]) > cb)
                                        if(*(cache_2+4) > cb)
                                            if(*(cache_0 + pixel[13]) > cb)
                                                if(*(cache_0 + pixel[0]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0 + pixel[0]) > cb)
                                        if(*(cache_0 + pixel[10]) > cb)
                                            if(*(cache_0 + pixel[13]) > cb)
                                                if(*(cache_2+4) > cb)
                                                    if(*(cache_0 + pixel[15]) > cb)
                                                        if(*(cache_0 + pixel[1]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else if(*(cache_2+4) < c_b)
                                                    continue;
                                                else
                                                    if(*(cache_0 + pixel[9]) > cb)
                                                        if(*(cache_0 + pixel[1]) > cb)
                                                            if(*(cache_0 + pixel[15]) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else if(*(cache_0 + pixel[1]) < c_b)
                                                            continue;
                                                        else
                                                            if(*(cache_0 + pixel[8]) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                    else
                                                        continue;
                                            else
                                                continue;
                                        else if(*(cache_0 + pixel[10]) < c_b)
                                            continue;
                                        else
                                            if(*(cache_0 + pixel[3]) > cb)
                                                if(*(cache_2+4) > cb)
                                                    if(*(cache_0 + pixel[15]) > cb)
                                                        if(*(cache_0 + pixel[13]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        continue;
                            else
                                continue;
                        else
                            continue;
                else if(*cache_2 < c_b)
                    if(*(cache_0+3) > cb)
                        if(*(cache_0 + pixel[7]) > cb)
                            if(*(cache_0 + pixel[1]) > cb)
                                if(*(cache_0 + pixel[9]) > cb)
                                    if(*(cache_2+4) > cb)
                                        if(*(cache_0 + pixel[6]) > cb)
                                            if(*(cache_0 + pixel[3]) > cb)
                                                if(*(cache_0 + pixel[8]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else if(*(cache_2+4) < c_b)
                                        continue;
                                    else
                                        if(*(cache_1+-6) > cb)
                                            if(*(cache_0 + pixel[3]) > cb)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                else if(*(cache_0 + pixel[9]) < c_b)
                                    if(*(cache_0 + pixel[15]) > cb)
                                        if(*(cache_2+4) > cb)
                                            if(*(cache_0 + pixel[3]) > cb)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0 + pixel[0]) > cb)
                                        if(*(cache_0 + pixel[8]) > cb)
                                            if(*(cache_2+4) > cb)
                                                if(*(cache_0 + pixel[3]) > cb)
                                                    if(*(cache_0 + pixel[6]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else if(*(cache_0 + pixel[8]) < c_b)
                                            continue;
                                        else
                                            if(*(cache_0 + pixel[15]) > cb)
                                                if(*(cache_2+4) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        continue;
                            else if(*(cache_0 + pixel[1]) < c_b)
                                if(*(cache_1+-6) > cb)
                                    if(*(cache_0 + pixel[3]) > cb)
                                        if(*(cache_0 + pixel[10]) > cb)
                                            if(*(cache_0 + pixel[6]) > cb)
                                                if(*(cache_0 + pixel[8]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else if(*(cache_0 + pixel[3]) < c_b)
                                        continue;
                                    else
                                        if(*(cache_0+-3) > cb)
                                            if(*(cache_0 + pixel[10]) > cb)
                                                if(*(cache_0 + pixel[6]) > cb)
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else if(*(cache_1+-6) < c_b)
                                    if(*(cache_0 + pixel[9]) > cb)
                                        if(*(cache_0 + pixel[3]) > cb)
                                            if(*(cache_2+4) > cb)
                                                if(*(cache_0 + pixel[10]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else if(*(cache_2+4) < c_b)
                                                if(*(cache_0 + pixel[10]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else if(*(cache_0 + pixel[3]) < c_b)
                                            if(*(cache_0 + pixel[15]) < c_b)
                                                if(*(cache_0+-3) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            if(*(cache_0 + pixel[10]) < c_b)
                                                if(*(cache_2+4) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else if(*(cache_0 + pixel[9]) < c_b)
                                        if(*(cache_0 + pixel[0]) < c_b)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        if(*(cache_2+4) < c_b)
                                            if(*(cache_0 + pixel[10]) > cb)
                                                continue;
                                            else if(*(cache_0 + pixel[10]) < c_b)
                                                if(*(cache_0 + pixel[15]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                if(*(cache_0 + pixel[3]) < c_b)
                                                    if(*(cache_0 + pixel[15]) < c_b)
                                                        if(*(cache_0 + pixel[0]) < c_b)
                                                            if(*(cache_0+-3) < c_b)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            continue;
                                else
                                    if(*(cache_2+4) > cb)
                                        if(*(cache_0 + pixel[8]) > cb)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                if(*(cache_0 + pixel[10]) > cb)
                                    if(*(cache_0 + pixel[3]) > cb)
                                        if(*(cache_2+4) > cb)
                                            if(*(cache_0 + pixel[6]) > cb)
                                                if(*(cache_0 + pixel[9]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else if(*(cache_2+4) < c_b)
                                            continue;
                                        else
                                            if(*(cache_1+-6) > cb)
                                                if(*(cache_0 + pixel[6]) > cb)
                                                    if(*(cache_0 + pixel[9]) > cb)
                                                        if(*(cache_0 + pixel[8]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else if(*(cache_0 + pixel[3]) < c_b)
                                        continue;
                                    else
                                        if(*(cache_0+-3) > cb)
                                            if(*(cache_1+-6) > cb)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    continue;
                        else if(*(cache_0 + pixel[7]) < c_b)
                            if(*(cache_1+-6) < c_b)
                                if(*(cache_0 + pixel[15]) > cb)
                                    continue;
                                else if(*(cache_0 + pixel[15]) < c_b)
                                    if(*(cache_0+-3) < c_b)
                                        if(*(cache_0 + pixel[10]) > cb)
                                            continue;
                                        else if(*(cache_0 + pixel[10]) < c_b)
                                            if(*(cache_0 + pixel[13]) < c_b)
                                                if(*(cache_0 + pixel[9]) > cb)
                                                    continue;
                                                else if(*(cache_0 + pixel[9]) < c_b)
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        continue;
                                                    else if(*(cache_0 + pixel[8]) < c_b)
                                                        goto success;
                                                    else
                                                        if(*(cache_0 + pixel[1]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                else
                                                    if(*(cache_2+4) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                            else
                                                continue;
                                        else
                                            if(*(cache_0 + pixel[3]) < c_b)
                                                goto success;
                                            else
                                                continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0 + pixel[6]) < c_b)
                                        if(*(cache_0 + pixel[10]) < c_b)
                                            if(*(cache_0+-3) < c_b)
                                                if(*(cache_0 + pixel[8]) < c_b)
                                                    if(*(cache_0 + pixel[13]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                continue;
                        else
                            if(*(cache_0 + pixel[0]) < c_b)
                                if(*(cache_0 + pixel[10]) > cb)
                                    continue;
                                else if(*(cache_0 + pixel[10]) < c_b)
                                    if(*(cache_0 + pixel[9]) > cb)
                                        continue;
                                    else if(*(cache_0 + pixel[9]) < c_b)
                                        if(*(cache_0+-3) < c_b)
                                            if(*(cache_0 + pixel[1]) > cb)
                                                continue;
                                            else if(*(cache_0 + pixel[1]) < c_b)
                                                if(*(cache_1+-6) < c_b)
                                                    if(*(cache_0 + pixel[13]) < c_b)
                                                        if(*(cache_0 + pixel[15]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                if(*(cache_0 + pixel[8]) < c_b)
                                                    if(*(cache_0 + pixel[13]) < c_b)
                                                        if(*(cache_1+-6) < c_b)
                                                            if(*(cache_0 + pixel[15]) < c_b)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            continue;
                                    else
                                        if(*(cache_2+4) < c_b)
                                            if(*(cache_0+-3) < c_b)
                                                if(*(cache_0 + pixel[1]) < c_b)
                                                    if(*(cache_1+-6) < c_b)
                                                        if(*(cache_0 + pixel[13]) < c_b)
                                                            if(*(cache_0 + pixel[15]) < c_b)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    if(*(cache_0 + pixel[3]) < c_b)
                                        if(*(cache_1+-6) < c_b)
                                            if(*(cache_0+-3) < c_b)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                continue;
                    else if(*(cache_0+3) < c_b)
                        if(*(cache_0+-3) > cb)
                            if(*(cache_0 + pixel[13]) > cb)
                                goto success;
                            else
                                continue;
                        else if(*(cache_0+-3) < c_b)
                            if(*(cache_0 + pixel[9]) > cb)
                                if(*(cache_0 + pixel[13]) < c_b)
                                    goto success;
                                else
                                    continue;
                            else if(*(cache_0 + pixel[9]) < c_b)
                                goto success;
                            else
                                if(*(cache_0 + pixel[6]) > cb || *(cache_0 + pixel[6]) < c_b)
                                    continue;
                                else
                                    if(*(cache_2+4) < c_b)
                                        goto success;
                                    else
                                        continue;
                        else
                            continue;
                    else
                        if(*(cache_1+-6) > cb)
                            if(*(cache_0 + pixel[13]) > cb)
                                if(*(cache_0 + pixel[9]) > cb)
                                    if(*(cache_0 + pixel[7]) > cb)
                                        if(*(cache_0+-3) > cb)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                continue;
                        else if(*(cache_1+-6) < c_b)
                            if(*(cache_0 + pixel[3]) > cb)
                                if(*(cache_0 + pixel[8]) < c_b)
                                    if(*(cache_0 + pixel[15]) > cb)
                                        continue;
                                    else if(*(cache_0 + pixel[15]) < c_b)
                                        if(*(cache_0 + pixel[13]) < c_b)
                                            if(*(cache_0 + pixel[0]) > cb)
                                                continue;
                                            else if(*(cache_0 + pixel[0]) < c_b)
                                                goto success;
                                            else
                                                if(*(cache_0 + pixel[7]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                        else
                                            continue;
                                    else
                                        if(*(cache_0 + pixel[6]) < c_b)
                                            goto success;
                                        else
                                            continue;
                                else
                                    continue;
                            else if(*(cache_0 + pixel[3]) < c_b)
                                if(*(cache_2+4) > cb)
                                    continue;
                                else if(*(cache_2+4) < c_b)
                                    if(*(cache_0 + pixel[0]) < c_b)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            continue;
                                        else if(*(cache_0 + pixel[1]) < c_b)
                                            if(*(cache_0 + pixel[15]) < c_b)
                                                if(*(cache_0+-3) < c_b)
                                                    if(*(cache_0 + pixel[13]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            if(*(cache_0 + pixel[8]) < c_b)
                                                goto success;
                                            else
                                                continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0 + pixel[9]) < c_b)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            continue;
                                        else if(*(cache_0 + pixel[1]) < c_b)
                                            if(*(cache_0+-3) < c_b)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            if(*(cache_0 + pixel[8]) < c_b)
                                                if(*(cache_0 + pixel[0]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        continue;
                            else
                                if(*(cache_0 + pixel[1]) > cb)
                                    continue;
                                else if(*(cache_0 + pixel[1]) < c_b)
                                    if(*(cache_0 + pixel[10]) < c_b)
                                        if(*(cache_0+-3) < c_b)
                                            if(*(cache_0 + pixel[9]) > cb)
                                                if(*(cache_2+4) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else if(*(cache_0 + pixel[9]) < c_b)
                                                if(*(cache_0 + pixel[15]) > cb)
                                                    continue;
                                                else if(*(cache_0 + pixel[15]) < c_b)
                                                    if(*(cache_0 + pixel[13]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    if(*(cache_0 + pixel[6]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                            else
                                                if(*(cache_2+4) < c_b)
                                                    if(*(cache_0 + pixel[15]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0 + pixel[7]) > cb)
                                        continue;
                                    else if(*(cache_0 + pixel[7]) < c_b)
                                        if(*(cache_0 + pixel[15]) > cb)
                                            continue;
                                        else if(*(cache_0 + pixel[15]) < c_b)
                                            if(*(cache_0 + pixel[10]) < c_b)
                                                if(*(cache_0+-3) < c_b)
                                                    if(*(cache_0 + pixel[8]) < c_b)
                                                        if(*(cache_0 + pixel[13]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            if(*(cache_0 + pixel[6]) < c_b)
                                                goto success;
                                            else
                                                continue;
                                    else
                                        if(*(cache_0 + pixel[0]) < c_b)
                                            if(*(cache_0 + pixel[8]) < c_b)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                        else
                            continue;
                else
                    if(*(cache_0 + pixel[7]) > cb)
                        if(*(cache_0 + pixel[3]) > cb)
                            if(*(cache_0 + pixel[10]) > cb)
                                if(*(cache_0+3) > cb)
                                    if(*(cache_2+4) > cb)
                                        if(*(cache_0 + pixel[6]) > cb)
                                            if(*(cache_0 + pixel[8]) > cb)
                                                if(*(cache_0 + pixel[9]) > cb)
                                                    goto success;
                                                else if(*(cache_0 + pixel[9]) < c_b)
                                                    continue;
                                                else
                                                    if(*(cache_0 + pixel[0]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                            else if(*(cache_0 + pixel[8]) < c_b)
                                                continue;
                                            else
                                                if(*(cache_0 + pixel[15]) > cb)
                                                    if(*(cache_0 + pixel[0]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            continue;
                                    else if(*(cache_2+4) < c_b)
                                        if(*(cache_1+-6) > cb)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        if(*(cache_1+-6) > cb)
                                            if(*(cache_0 + pixel[6]) > cb)
                                                if(*(cache_0 + pixel[8]) > cb)
                                                    if(*(cache_0 + pixel[9]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else if(*(cache_0+3) < c_b)
                                    continue;
                                else
                                    if(*(cache_0+-3) > cb)
                                        if(*(cache_0 + pixel[13]) > cb)
                                            if(*(cache_1+-6) > cb)
                                                if(*(cache_0 + pixel[6]) > cb)
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        if(*(cache_0 + pixel[9]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else if(*(cache_0 + pixel[10]) < c_b)
                                if(*(cache_0 + pixel[15]) > cb)
                                    if(*(cache_2+4) > cb)
                                        if(*(cache_0 + pixel[6]) > cb)
                                            if(*(cache_0+3) > cb)
                                                if(*(cache_0 + pixel[0]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else if(*(cache_0 + pixel[15]) < c_b)
                                    continue;
                                else
                                    if(*(cache_0 + pixel[8]) > cb)
                                        if(*(cache_0 + pixel[0]) > cb)
                                            goto success;
                                        else if(*(cache_0 + pixel[0]) < c_b)
                                            continue;
                                        else
                                            if(*(cache_0 + pixel[9]) > cb)
                                                if(*(cache_0 + pixel[1]) > cb)
                                                    if(*(cache_0 + pixel[6]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        continue;
                            else
                                if(*(cache_0 + pixel[1]) > cb)
                                    if(*(cache_0 + pixel[9]) > cb)
                                        if(*(cache_0 + pixel[6]) > cb)
                                            if(*(cache_0+3) > cb)
                                                if(*(cache_2+4) > cb)
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        goto success;
                                                    else if(*(cache_0 + pixel[8]) < c_b)
                                                        continue;
                                                    else
                                                        if(*(cache_0 + pixel[15]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else if(*(cache_0 + pixel[9]) < c_b)
                                        if(*(cache_0 + pixel[0]) > cb)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        if(*(cache_0 + pixel[0]) > cb)
                                            if(*(cache_0+3) > cb)
                                                if(*(cache_0 + pixel[6]) > cb)
                                                    if(*(cache_0 + pixel[15]) > cb)
                                                        if(*(cache_2+4) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else if(*(cache_0 + pixel[15]) < c_b)
                                                        continue;
                                                    else
                                                        if(*(cache_0 + pixel[8]) > cb)
                                                            if(*(cache_2+4) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    continue;
                        else if(*(cache_0 + pixel[3]) < c_b)
                            if(*(cache_0 + pixel[13]) > cb)
                                if(*(cache_1+-6) > cb)
                                    if(*(cache_0 + pixel[9]) > cb)
                                        if(*(cache_0+-3) > cb)
                                            if(*(cache_0 + pixel[6]) > cb)
                                                if(*(cache_0 + pixel[8]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else if(*(cache_0 + pixel[13]) < c_b)
                                continue;
                            else
                                if(*(cache_0+3) > cb)
                                    if(*(cache_0+-3) > cb)
                                        if(*(cache_0 + pixel[10]) > cb)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                        else
                            if(*(cache_0+-3) > cb)
                                if(*(cache_0 + pixel[13]) > cb)
                                    if(*(cache_1+-6) > cb)
                                        if(*(cache_0 + pixel[9]) > cb)
                                            if(*(cache_0 + pixel[6]) > cb)
                                                if(*(cache_0 + pixel[10]) > cb)
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else if(*(cache_0 + pixel[13]) < c_b)
                                    if(*(cache_0 + pixel[0]) > cb)
                                        goto success;
                                    else
                                        continue;
                                else
                                    if(*(cache_0+3) > cb)
                                        if(*(cache_0 + pixel[9]) > cb)
                                            if(*(cache_1+-6) > cb)
                                                if(*(cache_0 + pixel[6]) > cb)
                                                    if(*(cache_0 + pixel[10]) > cb)
                                                        if(*(cache_0 + pixel[8]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                continue;
                    else
                        continue;
            else if(*cache_1 < c_b)
                if(*(cache_0 + pixel[15]) > cb)
                    if(*(cache_1+-6) > cb)
                        if(*(cache_2+4) > cb)
                            if(*(cache_0+-3) > cb)
                                if(*(cache_0 + pixel[10]) > cb)
                                    if(*(cache_0 + pixel[13]) > cb)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            if(*cache_2 > cb)
                                                goto success;
                                            else
                                                continue;
                                        else if(*(cache_0 + pixel[1]) < c_b)
                                            continue;
                                        else
                                            if(*(cache_0 + pixel[7]) > cb)
                                                goto success;
                                            else
                                                continue;
                                    else
                                        continue;
                                else if(*(cache_0 + pixel[10]) < c_b)
                                    if(*(cache_0 + pixel[3]) > cb)
                                        if(*(cache_0 + pixel[13]) > cb)
                                            if(*cache_2 > cb)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0 + pixel[3]) > cb)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            if(*cache_2 > cb)
                                                if(*(cache_0 + pixel[0]) > cb)
                                                    if(*(cache_0 + pixel[13]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                continue;
                        else if(*(cache_2+4) < c_b)
                            if(*(cache_0 + pixel[7]) > cb)
                                if(*(cache_0+-3) > cb)
                                    if(*cache_2 > cb)
                                        if(*(cache_0 + pixel[13]) > cb)
                                            if(*(cache_0 + pixel[9]) > cb)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else if(*(cache_0 + pixel[7]) < c_b)
                                if(*(cache_0 + pixel[9]) > cb)
                                    if(*(cache_0 + pixel[1]) > cb)
                                        if(*(cache_0+-3) > cb)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else if(*(cache_0 + pixel[9]) < c_b)
                                    if(*(cache_0 + pixel[10]) > cb)
                                        continue;
                                    else if(*(cache_0 + pixel[10]) < c_b)
                                        if(*(cache_0 + pixel[3]) < c_b)
                                            if(*(cache_0+3) < c_b)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        if(*(cache_0 + pixel[1]) < c_b)
                                            if(*(cache_0 + pixel[3]) < c_b)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    if(*(cache_0 + pixel[0]) < c_b)
                                        goto success;
                                    else
                                        continue;
                            else
                                if(*(cache_0 + pixel[0]) > cb)
                                    if(*(cache_0 + pixel[13]) > cb)
                                        if(*(cache_0 + pixel[9]) > cb)
                                            if(*cache_2 > cb)
                                                if(*(cache_0 + pixel[1]) > cb)
                                                    if(*(cache_0 + pixel[10]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else if(*(cache_0 + pixel[1]) < c_b)
                                                    continue;
                                                else
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        if(*(cache_0+-3) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                        else
                            if(*(cache_0 + pixel[9]) > cb)
                                if(*(cache_0+-3) > cb)
                                    if(*(cache_0 + pixel[1]) > cb)
                                        if(*cache_2 > cb)
                                            if(*(cache_0 + pixel[10]) > cb)
                                                if(*(cache_0 + pixel[13]) > cb)
                                                    if(*(cache_0 + pixel[0]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else if(*(cache_0 + pixel[1]) < c_b)
                                        continue;
                                    else
                                        if(*(cache_0 + pixel[7]) > cb)
                                            if(*(cache_0 + pixel[10]) > cb)
                                                if(*(cache_0 + pixel[13]) > cb)
                                                    if(*cache_2 > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else if(*(cache_0 + pixel[7]) < c_b)
                                            continue;
                                        else
                                            if(*(cache_0 + pixel[0]) > cb)
                                                if(*(cache_0 + pixel[8]) > cb)
                                                    if(*(cache_0 + pixel[6]) < c_b)
                                                        if(*(cache_0 + pixel[10]) > cb)
                                                            if(*(cache_0 + pixel[13]) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                else
                                    continue;
                            else
                                continue;
                    else if(*(cache_1+-6) < c_b)
                        if(*(cache_0 + pixel[3]) > cb)
                            if(*(cache_0 + pixel[13]) > cb)
                                if(*(cache_0+-3) > cb)
                                    if(*(cache_0+3) > cb)
                                        goto success;
                                    else
                                        continue;
                                else if(*(cache_0+-3) < c_b)
                                    if(*(cache_0+3) < c_b)
                                        if(*(cache_0 + pixel[6]) < c_b)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else if(*(cache_0 + pixel[13]) < c_b)
                                if(*(cache_0 + pixel[7]) < c_b)
                                    if(*(cache_0 + pixel[6]) < c_b)
                                        if(*(cache_0 + pixel[8]) < c_b)
                                            if(*(cache_0+-3) < c_b)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                if(*(cache_0+3) < c_b)
                                    if(*(cache_0+-3) < c_b)
                                        if(*(cache_0 + pixel[7]) < c_b)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                        else if(*(cache_0 + pixel[3]) < c_b)
                            if(*(cache_0 + pixel[8]) < c_b)
                                if(*(cache_0 + pixel[9]) < c_b)
                                    if(*(cache_0 + pixel[7]) < c_b)
                                        if(*(cache_0+3) > cb)
                                            continue;
                                        else if(*(cache_0+3) < c_b)
                                            if(*(cache_0 + pixel[10]) > cb)
                                                continue;
                                            else if(*(cache_0 + pixel[10]) < c_b)
                                                if(*(cache_0 + pixel[6]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                if(*(cache_0 + pixel[1]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                        else
                                            if(*(cache_0 + pixel[13]) < c_b)
                                                goto success;
                                            else
                                                continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                continue;
                        else
                            if(*(cache_0+-3) < c_b)
                                if(*(cache_0+3) > cb)
                                    continue;
                                else if(*(cache_0+3) < c_b)
                                    if(*(cache_0 + pixel[6]) < c_b)
                                        if(*(cache_0 + pixel[10]) < c_b)
                                            if(*(cache_0 + pixel[9]) < c_b)
                                                if(*(cache_0 + pixel[7]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0 + pixel[13]) < c_b)
                                        if(*(cache_0 + pixel[7]) < c_b)
                                            if(*(cache_0 + pixel[6]) < c_b)
                                                if(*(cache_0 + pixel[10]) < c_b)
                                                    if(*(cache_0 + pixel[8]) < c_b)
                                                        if(*(cache_0 + pixel[9]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                continue;
                    else
                        if(*(cache_2+4) > cb)
                            if(*(cache_0+3) > cb)
                                if(*(cache_0+-3) > cb)
                                    if(*(cache_0 + pixel[13]) > cb)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            if(*(cache_0 + pixel[3]) > cb)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                continue;
                        else if(*(cache_2+4) < c_b)
                            if(*(cache_0 + pixel[10]) > cb)
                                continue;
                            else if(*(cache_0 + pixel[10]) < c_b)
                                if(*(cache_0+3) < c_b)
                                    if(*(cache_0 + pixel[9]) < c_b)
                                        if(*(cache_0 + pixel[3]) < c_b)
                                            if(*(cache_0 + pixel[7]) < c_b)
                                                if(*(cache_0 + pixel[6]) < c_b)
                                                    if(*(cache_0 + pixel[8]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                if(*(cache_0 + pixel[1]) < c_b)
                                    if(*(cache_0 + pixel[9]) < c_b)
                                        if(*(cache_0 + pixel[3]) < c_b)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                        else
                            continue;
                else if(*(cache_0 + pixel[15]) < c_b)
                    if(*(cache_0+3) > cb)
                        if(*(cache_0+-3) < c_b)
                            if(*(cache_1+-6) < c_b)
                                if(*(cache_0 + pixel[13]) < c_b)
                                    if(*(cache_0 + pixel[7]) > cb)
                                        continue;
                                    else if(*(cache_0 + pixel[7]) < c_b)
                                        goto success;
                                    else
                                        if(*(cache_0 + pixel[8]) < c_b)
                                            if(*(cache_0 + pixel[0]) < c_b)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    continue;
                            else
                                continue;
                        else
                            continue;
                    else if(*(cache_0+3) < c_b)
                        if(*(cache_0 + pixel[6]) > cb)
                            if(*(cache_0 + pixel[13]) > cb)
                                if(*cache_2 > cb)
                                    if(*(cache_0 + pixel[10]) > cb)
                                        goto success;
                                    else
                                        continue;
                                else
                                    continue;
                            else if(*(cache_0 + pixel[13]) < c_b)
                                if(*(cache_0 + pixel[0]) < c_b)
                                    if(*(cache_2+4) < c_b)
                                        if(*cache_2 < c_b)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                continue;
                        else if(*(cache_0 + pixel[6]) < c_b)
                            if(*(cache_0 + pixel[3]) > cb)
                                if(*(cache_0+-3) < c_b)
                                    if(*(cache_0 + pixel[1]) < c_b)
                                        continue;
                                    else
                                        goto success;
                                else
                                    continue;
                            else if(*(cache_0 + pixel[3]) < c_b)
                                if(*(cache_0 + pixel[7]) > cb)
                                    if(*cache_2 < c_b)
                                        goto success;
                                    else
                                        continue;
                                else if(*(cache_0 + pixel[7]) < c_b)
                                    if(*(cache_2+4) > cb)
                                        if(*(cache_0 + pixel[10]) < c_b)
                                            goto success;
                                        else
                                            continue;
                                    else if(*(cache_2+4) < c_b)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            continue;
                                        else if(*(cache_0 + pixel[1]) < c_b)
                                            if(*(cache_0 + pixel[0]) > cb)
                                                continue;
                                            else if(*(cache_0 + pixel[0]) < c_b)
                                                goto success;
                                            else
                                                if(*(cache_0 + pixel[9]) < c_b)
                                                    if(*(cache_0 + pixel[8]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            if(*(cache_0 + pixel[10]) < c_b)
                                                if(*(cache_0 + pixel[8]) < c_b)
                                                    if(*(cache_0 + pixel[9]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        if(*(cache_1+-6) < c_b)
                                            if(*(cache_0 + pixel[10]) < c_b)
                                                if(*(cache_0 + pixel[8]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    if(*cache_2 < c_b)
                                        if(*(cache_2+4) < c_b)
                                            if(*(cache_0 + pixel[0]) < c_b)
                                                if(*(cache_0 + pixel[1]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                if(*(cache_0+-3) < c_b)
                                    if(*(cache_1+-6) < c_b)
                                        if(*(cache_0 + pixel[10]) < c_b)
                                            if(*(cache_0 + pixel[8]) > cb)
                                                continue;
                                            else if(*(cache_0 + pixel[8]) < c_b)
                                                if(*(cache_0 + pixel[9]) > cb)
                                                    continue;
                                                else if(*(cache_0 + pixel[9]) < c_b)
                                                    if(*(cache_0 + pixel[7]) > cb)
                                                        continue;
                                                    else if(*(cache_0 + pixel[7]) < c_b)
                                                        goto success;
                                                    else
                                                        if(*(cache_0 + pixel[13]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                else
                                                    if(*(cache_2+4) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                            else
                                                if(*(cache_0 + pixel[13]) < c_b)
                                                    if(*(cache_0 + pixel[0]) < c_b)
                                                        if(*(cache_0 + pixel[7]) > cb || *(cache_0 + pixel[7]) < c_b)
                                                            continue;
                                                        else
                                                            goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                        else
                            if(*(cache_0 + pixel[13]) < c_b)
                                if(*(cache_2+4) > cb)
                                    continue;
                                else if(*(cache_2+4) < c_b)
                                    if(*cache_2 < c_b)
                                        if(*(cache_0 + pixel[3]) > cb)
                                            continue;
                                        else if(*(cache_0 + pixel[3]) < c_b)
                                            if(*(cache_0 + pixel[0]) > cb)
                                                continue;
                                            else if(*(cache_0 + pixel[0]) < c_b)
                                                if(*(cache_0 + pixel[1]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                if(*(cache_0 + pixel[7]) < c_b)
                                                    if(*(cache_1+-6) < c_b)
                                                        if(*(cache_0 + pixel[8]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            if(*(cache_0+-3) < c_b)
                                                if(*(cache_0 + pixel[10]) < c_b)
                                                    if(*(cache_0 + pixel[1]) > cb)
                                                        continue;
                                                    else if(*(cache_0 + pixel[1]) < c_b)
                                                        goto success;
                                                    else
                                                        if(*(cache_0 + pixel[7]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0 + pixel[9]) < c_b)
                                        if(*(cache_1+-6) < c_b)
                                            if(*(cache_0 + pixel[0]) > cb)
                                                continue;
                                            else if(*(cache_0 + pixel[0]) < c_b)
                                                if(*cache_2 < c_b)
                                                    if(*(cache_0 + pixel[10]) < c_b)
                                                        if(*(cache_0+-3) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                if(*(cache_0 + pixel[7]) < c_b)
                                                    if(*(cache_0 + pixel[8]) < c_b)
                                                        if(*(cache_0 + pixel[1]) > cb || *(cache_0 + pixel[1]) < c_b)
                                                            continue;
                                                        else
                                                            goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                continue;
                    else
                        if(*(cache_0+-3) < c_b)
                            if(*(cache_0 + pixel[13]) < c_b)
                                if(*(cache_1+-6) < c_b)
                                    if(*(cache_0 + pixel[9]) > cb)
                                        if(*(cache_0 + pixel[3]) < c_b)
                                            if(*(cache_2+4) < c_b)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else if(*(cache_0 + pixel[9]) < c_b)
                                        if(*(cache_0 + pixel[10]) > cb)
                                            continue;
                                        else if(*(cache_0 + pixel[10]) < c_b)
                                            if(*(cache_0 + pixel[7]) > cb)
                                                continue;
                                            else if(*(cache_0 + pixel[7]) < c_b)
                                                if(*cache_2 > cb || *cache_2 < c_b)
                                                    goto success;
                                                else
                                                    if(*(cache_0 + pixel[6]) < c_b)
                                                        if(*(cache_0 + pixel[8]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                            else
                                                if(*(cache_0 + pixel[1]) > cb)
                                                    continue;
                                                else if(*(cache_0 + pixel[1]) < c_b)
                                                    if(*cache_2 < c_b)
                                                        if(*(cache_0 + pixel[0]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    if(*(cache_0 + pixel[0]) < c_b)
                                                        if(*(cache_0 + pixel[8]) < c_b)
                                                            if(*cache_2 < c_b)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                        else
                                            if(*(cache_0 + pixel[3]) < c_b)
                                                goto success;
                                            else
                                                continue;
                                    else
                                        if(*(cache_2+4) < c_b)
                                            if(*(cache_0 + pixel[1]) < c_b)
                                                if(*(cache_0 + pixel[10]) > cb)
                                                    continue;
                                                else if(*(cache_0 + pixel[10]) < c_b)
                                                    if(*cache_2 < c_b)
                                                        if(*(cache_0 + pixel[0]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    if(*(cache_0 + pixel[3]) < c_b)
                                                        if(*(cache_0 + pixel[0]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    continue;
                            else
                                continue;
                        else
                            continue;
                else
                    if(*(cache_0 + pixel[8]) > cb)
                        if(*(cache_0 + pixel[6]) > cb)
                            if(*cache_2 > cb)
                                if(*(cache_1+-6) > cb)
                                    if(*(cache_0 + pixel[10]) > cb)
                                        goto success;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                continue;
                        else
                            continue;
                    else if(*(cache_0 + pixel[8]) < c_b)
                        if(*(cache_0 + pixel[3]) > cb)
                            if(*(cache_0 + pixel[13]) > cb)
                                continue;
                            else if(*(cache_0 + pixel[13]) < c_b)
                                if(*(cache_0+-3) < c_b)
                                    if(*(cache_0 + pixel[7]) < c_b)
                                        if(*(cache_1+-6) < c_b)
                                            if(*(cache_0 + pixel[6]) < c_b)
                                                if(*(cache_0 + pixel[10]) < c_b)
                                                    if(*(cache_0 + pixel[9]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                if(*(cache_0+3) < c_b)
                                    if(*(cache_0+-3) < c_b)
                                        if(*(cache_0 + pixel[10]) < c_b)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                        else if(*(cache_0 + pixel[3]) < c_b)
                            if(*(cache_2+4) > cb)
                                if(*(cache_1+-6) < c_b)
                                    if(*(cache_0 + pixel[7]) < c_b)
                                        goto success;
                                    else
                                        continue;
                                else
                                    continue;
                            else if(*(cache_2+4) < c_b)
                                if(*(cache_0 + pixel[6]) < c_b)
                                    if(*(cache_0+3) > cb)
                                        continue;
                                    else if(*(cache_0+3) < c_b)
                                        if(*(cache_0 + pixel[10]) > cb)
                                            if(*(cache_0 + pixel[0]) > cb)
                                                continue;
                                            else if(*(cache_0 + pixel[0]) < c_b)
                                                if(*(cache_0 + pixel[1]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                if(*(cache_0 + pixel[9]) < c_b)
                                                    if(*(cache_0 + pixel[1]) < c_b)
                                                        if(*(cache_0 + pixel[7]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else if(*(cache_0 + pixel[10]) < c_b)
                                            if(*(cache_0 + pixel[7]) < c_b)
                                                if(*(cache_0 + pixel[9]) > cb)
                                                    continue;
                                                else if(*(cache_0 + pixel[9]) < c_b)
                                                    goto success;
                                                else
                                                    if(*(cache_0 + pixel[0]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                            else
                                                continue;
                                        else
                                            if(*(cache_0 + pixel[1]) < c_b)
                                                if(*(cache_0 + pixel[9]) > cb)
                                                    continue;
                                                else if(*(cache_0 + pixel[9]) < c_b)
                                                    if(*(cache_0 + pixel[7]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    if(*(cache_0 + pixel[0]) < c_b)
                                                        if(*(cache_0 + pixel[7]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                            else
                                                continue;
                                    else
                                        if(*(cache_0+-3) < c_b)
                                            if(*(cache_0 + pixel[13]) < c_b)
                                                if(*(cache_1+-6) < c_b)
                                                    if(*(cache_0 + pixel[7]) < c_b)
                                                        if(*(cache_0 + pixel[10]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    continue;
                            else
                                if(*(cache_1+-6) < c_b)
                                    if(*(cache_0+3) > cb)
                                        continue;
                                    else if(*(cache_0+3) < c_b)
                                        if(*(cache_0 + pixel[6]) < c_b)
                                            if(*(cache_0 + pixel[10]) < c_b)
                                                if(*(cache_0 + pixel[7]) < c_b)
                                                    if(*(cache_0 + pixel[9]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        if(*(cache_0+-3) < c_b)
                                            if(*(cache_0 + pixel[13]) < c_b)
                                                if(*(cache_0 + pixel[6]) < c_b)
                                                    if(*(cache_0 + pixel[7]) < c_b)
                                                        if(*(cache_0 + pixel[10]) < c_b)
                                                            if(*(cache_0 + pixel[9]) < c_b)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    continue;
                        else
                            if(*(cache_0+-3) < c_b)
                                if(*(cache_0 + pixel[13]) > cb)
                                    if(*(cache_0+3) < c_b)
                                        goto success;
                                    else
                                        continue;
                                else if(*(cache_0 + pixel[13]) < c_b)
                                    if(*(cache_1+-6) < c_b)
                                        if(*(cache_0 + pixel[7]) < c_b)
                                            if(*(cache_0 + pixel[10]) < c_b)
                                                if(*(cache_0 + pixel[6]) < c_b)
                                                    if(*(cache_0 + pixel[9]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0+3) < c_b)
                                        if(*(cache_0 + pixel[10]) < c_b)
                                            if(*(cache_0 + pixel[6]) < c_b)
                                                if(*(cache_1+-6) < c_b)
                                                    if(*(cache_0 + pixel[7]) < c_b)
                                                        if(*(cache_0 + pixel[9]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                continue;
                    else
                        continue;
            else
                if(*(cache_0+-3) > cb)
                    if(*cache_2 > cb)
                        if(*(cache_0 + pixel[7]) > cb)
                            if(*(cache_1+-6) > cb)
                                if(*(cache_0 + pixel[6]) > cb)
                                    if(*(cache_0 + pixel[13]) > cb)
                                        if(*(cache_0 + pixel[10]) > cb)
                                            if(*(cache_0 + pixel[9]) > cb)
                                                if(*(cache_0 + pixel[8]) > cb)
                                                    goto success;
                                                else if(*(cache_0 + pixel[8]) < c_b)
                                                    continue;
                                                else
                                                    if(*(cache_0 + pixel[0]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                            else if(*(cache_0 + pixel[9]) < c_b)
                                                continue;
                                            else
                                                if(*(cache_2+4) > cb)
                                                    if(*(cache_0 + pixel[0]) > cb)
                                                        if(*(cache_0 + pixel[1]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else if(*(cache_0 + pixel[10]) < c_b)
                                            continue;
                                        else
                                            if(*(cache_0 + pixel[3]) > cb)
                                                if(*(cache_0 + pixel[0]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        continue;
                                else if(*(cache_0 + pixel[6]) < c_b)
                                    continue;
                                else
                                    if(*(cache_0 + pixel[15]) > cb)
                                        if(*(cache_0 + pixel[10]) > cb)
                                            if(*(cache_0 + pixel[13]) > cb)
                                                if(*(cache_0 + pixel[9]) > cb)
                                                    if(*(cache_0 + pixel[8]) > cb)
                                                        goto success;
                                                    else if(*(cache_0 + pixel[8]) < c_b)
                                                        continue;
                                                    else
                                                        if(*(cache_0 + pixel[1]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                else if(*(cache_0 + pixel[9]) < c_b)
                                                    continue;
                                                else
                                                    if(*(cache_2+4) > cb)
                                                        if(*(cache_0 + pixel[1]) > cb)
                                                            if(*(cache_0 + pixel[0]) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                            else
                                                continue;
                                        else if(*(cache_0 + pixel[10]) < c_b)
                                            continue;
                                        else
                                            if(*(cache_0 + pixel[3]) > cb)
                                                if(*(cache_0 + pixel[1]) > cb)
                                                    if(*(cache_2+4) > cb)
                                                        if(*(cache_0 + pixel[13]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        continue;
                            else if(*(cache_1+-6) < c_b)
                                continue;
                            else
                                if(*(cache_0+3) > cb)
                                    if(*(cache_2+4) > cb)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            if(*(cache_0 + pixel[0]) > cb)
                                                if(*(cache_0 + pixel[3]) > cb)
                                                    if(*(cache_0 + pixel[13]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                        else if(*(cache_0 + pixel[7]) < c_b)
                            if(*(cache_2+4) > cb)
                                if(*(cache_1+-6) > cb)
                                    if(*(cache_0 + pixel[3]) > cb)
                                        if(*(cache_0 + pixel[15]) > cb)
                                            if(*(cache_0 + pixel[13]) > cb)
                                                if(*(cache_0 + pixel[1]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else if(*(cache_0 + pixel[3]) < c_b)
                                        continue;
                                    else
                                        if(*(cache_0 + pixel[10]) > cb)
                                            if(*(cache_0 + pixel[13]) > cb)
                                                if(*(cache_0 + pixel[0]) > cb)
                                                    if(*(cache_0 + pixel[1]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                else if(*(cache_1+-6) < c_b)
                                    if(*(cache_0+3) > cb)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            if(*(cache_0 + pixel[0]) > cb)
                                                if(*(cache_0 + pixel[3]) > cb)
                                                    goto success;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0+3) > cb)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            if(*(cache_0 + pixel[13]) > cb)
                                                if(*(cache_0 + pixel[3]) > cb)
                                                    if(*(cache_0 + pixel[0]) > cb)
                                                        if(*(cache_0 + pixel[15]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else if(*(cache_2+4) < c_b)
                                continue;
                            else
                                if(*(cache_0 + pixel[9]) > cb)
                                    if(*(cache_0 + pixel[0]) > cb)
                                        if(*(cache_1+-6) > cb)
                                            goto success;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                        else
                            if(*(cache_0 + pixel[0]) > cb)
                                if(*(cache_0 + pixel[10]) > cb)
                                    if(*(cache_2+4) > cb)
                                        if(*(cache_0 + pixel[13]) > cb)
                                            if(*(cache_1+-6) > cb)
                                                if(*(cache_0 + pixel[15]) > cb)
                                                    if(*(cache_0 + pixel[1]) > cb)
                                                        goto success;
                                                    else if(*(cache_0 + pixel[1]) < c_b)
                                                        continue;
                                                    else
                                                        if(*(cache_0 + pixel[8]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                else
                                                    continue;
                                            else if(*(cache_1+-6) < c_b)
                                                continue;
                                            else
                                                if(*(cache_0+3) > cb)
                                                    if(*(cache_0 + pixel[15]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            continue;
                                    else if(*(cache_2+4) < c_b)
                                        if(*(cache_0 + pixel[1]) > cb)
                                            if(*(cache_0 + pixel[3]) < c_b)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        if(*(cache_0 + pixel[9]) > cb)
                                            if(*(cache_0 + pixel[1]) > cb)
                                                if(*(cache_0 + pixel[13]) > cb)
                                                    if(*(cache_0 + pixel[15]) > cb)
                                                        if(*(cache_1+-6) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else if(*(cache_0 + pixel[1]) < c_b)
                                                continue;
                                            else
                                                if(*(cache_0 + pixel[8]) > cb)
                                                    if(*(cache_1+-6) > cb)
                                                        if(*(cache_0 + pixel[13]) > cb)
                                                            if(*(cache_0 + pixel[15]) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                        else
                                            continue;
                                else if(*(cache_0 + pixel[10]) < c_b)
                                    if(*(cache_0+3) > cb)
                                        if(*(cache_0 + pixel[13]) > cb)
                                            if(*(cache_2+4) > cb)
                                                if(*(cache_0 + pixel[3]) > cb)
                                                    if(*(cache_0 + pixel[15]) > cb)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else if(*(cache_0+3) < c_b)
                                        continue;
                                    else
                                        if(*(cache_1+-6) > cb)
                                            if(*(cache_0 + pixel[3]) > cb)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    if(*(cache_0 + pixel[3]) > cb)
                                        if(*(cache_1+-6) > cb)
                                            if(*(cache_0 + pixel[13]) > cb)
                                                if(*(cache_2+4) > cb)
                                                    if(*(cache_0 + pixel[15]) > cb)
                                                        if(*(cache_0 + pixel[1]) > cb)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else if(*(cache_1+-6) < c_b)
                                            if(*(cache_0+3) > cb)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            if(*(cache_0+3) > cb)
                                                if(*(cache_0 + pixel[13]) > cb)
                                                    if(*(cache_0 + pixel[1]) > cb)
                                                        if(*(cache_2+4) > cb)
                                                            if(*(cache_0 + pixel[15]) > cb)
                                                                goto success;
                                                            else
                                                                continue;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        continue;
                            else
                                continue;
                    else
                        continue;
                else if(*(cache_0+-3) < c_b)
                    if(*(cache_0 + pixel[15]) > cb)
                        if(*cache_2 < c_b)
                            if(*(cache_0 + pixel[6]) < c_b)
                                if(*(cache_0 + pixel[10]) < c_b)
                                    if(*(cache_0 + pixel[7]) < c_b)
                                        goto success;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                continue;
                        else
                            continue;
                    else if(*(cache_0 + pixel[15]) < c_b)
                        if(*(cache_0 + pixel[10]) > cb)
                            if(*(cache_0+3) > cb)
                                continue;
                            else if(*(cache_0+3) < c_b)
                                if(*(cache_0 + pixel[3]) < c_b)
                                    if(*(cache_0 + pixel[13]) < c_b)
                                        goto success;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                if(*(cache_1+-6) < c_b)
                                    if(*(cache_0 + pixel[3]) < c_b)
                                        goto success;
                                    else
                                        continue;
                                else
                                    continue;
                        else if(*(cache_0 + pixel[10]) < c_b)
                            if(*cache_2 < c_b)
                                if(*(cache_0 + pixel[9]) > cb)
                                    if(*(cache_2+4) < c_b)
                                        goto success;
                                    else
                                        continue;
                                else if(*(cache_0 + pixel[9]) < c_b)
                                    if(*(cache_1+-6) > cb)
                                        continue;
                                    else if(*(cache_1+-6) < c_b)
                                        if(*(cache_0 + pixel[13]) < c_b)
                                            if(*(cache_0 + pixel[1]) > cb)
                                                if(*(cache_0 + pixel[7]) < c_b)
                                                    goto success;
                                                else
                                                    continue;
                                            else if(*(cache_0 + pixel[1]) < c_b)
                                                if(*(cache_0 + pixel[0]) > cb)
                                                    continue;
                                                else if(*(cache_0 + pixel[0]) < c_b)
                                                    goto success;
                                                else
                                                    if(*(cache_0 + pixel[7]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                            else
                                                if(*(cache_0 + pixel[7]) > cb)
                                                    continue;
                                                else if(*(cache_0 + pixel[7]) < c_b)
                                                    if(*(cache_0 + pixel[8]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    if(*(cache_0 + pixel[0]) < c_b)
                                                        if(*(cache_0 + pixel[8]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                        else
                                            continue;
                                    else
                                        if(*(cache_0+3) < c_b)
                                            if(*(cache_0 + pixel[3]) < c_b)
                                                goto success;
                                            else
                                                continue;
                                        else
                                            continue;
                                else
                                    if(*(cache_2+4) < c_b)
                                        if(*(cache_1+-6) > cb)
                                            continue;
                                        else if(*(cache_1+-6) < c_b)
                                            if(*(cache_0 + pixel[13]) < c_b)
                                                if(*(cache_0 + pixel[1]) < c_b)
                                                    if(*(cache_0 + pixel[0]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            if(*(cache_0+3) < c_b)
                                                if(*(cache_0 + pixel[3]) < c_b)
                                                    if(*(cache_0 + pixel[0]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                    else
                                        continue;
                            else
                                continue;
                        else
                            if(*(cache_0 + pixel[3]) < c_b)
                                if(*(cache_1+-6) > cb)
                                    continue;
                                else if(*(cache_1+-6) < c_b)
                                    if(*(cache_2+4) < c_b)
                                        if(*(cache_0 + pixel[13]) < c_b)
                                            if(*cache_2 < c_b)
                                                if(*(cache_0 + pixel[1]) < c_b)
                                                    if(*(cache_0 + pixel[0]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    if(*(cache_0+3) < c_b)
                                        if(*(cache_2+4) < c_b)
                                            if(*cache_2 < c_b)
                                                if(*(cache_0 + pixel[1]) < c_b)
                                                    if(*(cache_0 + pixel[13]) < c_b)
                                                        if(*(cache_0 + pixel[0]) < c_b)
                                                            goto success;
                                                        else
                                                            continue;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                            else
                                continue;
                    else
                        if(*(cache_0 + pixel[6]) < c_b)
                            if(*cache_2 < c_b)
                                if(*(cache_0 + pixel[7]) < c_b)
                                    if(*(cache_1+-6) < c_b)
                                        if(*(cache_0 + pixel[13]) < c_b)
                                            if(*(cache_0 + pixel[10]) < c_b)
                                                if(*(cache_0 + pixel[9]) < c_b)
                                                    if(*(cache_0 + pixel[8]) < c_b)
                                                        goto success;
                                                    else
                                                        continue;
                                                else
                                                    continue;
                                            else
                                                continue;
                                        else
                                            continue;
                                    else
                                        continue;
                                else
                                    continue;
                            else
                                continue;
                        else
                            continue;
                else
                    continue;
			success:																			
				if(total >= rsize)																
				{																				
					rsize *=2;																	
					ret=(xy*)realloc(ret, rsize*sizeof(xy));									
				}																				
				ret[total].x = cache_0-line_min;												
				ret[total++].y = y;																
		}																						
	}																							
	*num = total;																				
	return ret;																					
}																								
																								
