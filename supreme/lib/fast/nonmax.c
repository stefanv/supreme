#include <stdlib.h>
#include "fast.h"

int corner_score(const byte*  imp, const int *pointer_dir, int barrier)
{
	/*The score for a positive feature is sum of the difference between the pixels
	  and the barrier if the difference is positive. Negative is similar.
	  The score is the max of those two.
	  
	   B = {x | x = points on the Bresenham circle around c}
	   Sp = { I(x) - t | x E B , I(x) - t > 0 }
	   Sn = { t - I(x) | x E B, t - I(x) > 0}
	  
	   Score = max sum(Sp), sum(Sn)*/

	int cb = *imp + barrier;
	int c_b = *imp - barrier;
	int sp=0, sn = 0;

	int i=0;

	for(i=0; i<16; i++)
	{
		int p = imp[pointer_dir[i]];

		if(p > cb)
			sp += p-cb;
		else if(p < c_b)
			sn += c_b-p;
	}
	
	if(sp > sn)
		return sp;
	else 
		return sn;
}

/*void fast_nonmax(const BasicImage<byte>& im, const vector<ImageRef>& corners, int barrier, vector<ReturnType>& nonmax_corners)*/
xy*  fast_nonmax(const byte* im, int xsize, int ysize, xy* corners, int numcorners, int barrier, int* numnx)
{
  
	/*Create a list of integer pointer offstes, corresponding to the */
	/*direction offsets in dir[]*/
	int	pointer_dir[16];
	int* row_start = (int*) malloc(ysize * sizeof(int));
	int* scores    = (int*) malloc(numcorners * sizeof(int));
	xy*  nonmax_corners=(xy*)malloc(numcorners* sizeof(xy));
	int num_nonmax=0;
	int prev_row = -1;
	int i, j;
	int point_above = 0;
	int point_below = 0;


	pointer_dir[0] = 0 + 3 * xsize;		
	pointer_dir[1] = 1 + 3 * xsize;		
	pointer_dir[2] = 2 + 2 * xsize;		
	pointer_dir[3] = 3 + 1 * xsize;		
	pointer_dir[4] = 3 + 0 * xsize;		
	pointer_dir[5] = 3 + -1 * xsize;		
	pointer_dir[6] = 2 + -2 * xsize;		
	pointer_dir[7] = 1 + -3 * xsize;		
	pointer_dir[8] = 0 + -3 * xsize;		
	pointer_dir[9] = -1 + -3 * xsize;		
	pointer_dir[10] = -2 + -2 * xsize;		
	pointer_dir[11] = -3 + -1 * xsize;		
	pointer_dir[12] = -3 + 0 * xsize;		
	pointer_dir[13] = -3 + 1 * xsize;		
	pointer_dir[14] = -2 + 2 * xsize;		
	pointer_dir[15] = -1 + 3 * xsize;		

	if(numcorners < 5)
	{
		free(row_start);
		free(scores);
		free(nonmax_corners);
		return 0;
	}

	/*xsize ysize numcorners corners*/

	/*Compute the score for each detected corner, and find where each row begins*/
	/* (the corners are output in raster scan order). A beginning of -1 signifies*/
	/* that there are no corners on that row.*/

  
	for(i=0; i <ysize; i++)
		row_start[i] = -1;
	  
	  
	for(i=0; i< numcorners; i++)
	{
		if(corners[i].y != prev_row)
		{
			row_start[corners[i].y] = i;
			prev_row = corners[i].y;
		}
		  
		scores[i] = corner_score(im + corners[i].x + corners[i].y * xsize, pointer_dir, barrier);
	}
  
  
	/*Point above points (roughly) to the pixel above the one of interest, if there*/
	/*is a feature there.*/
  
  
	for(i=1; i < numcorners-1; i++)
	{
		int score = scores[i];
		xy pos = corners[i];

		/*Check left*/
		/*if(corners[i-1] == pos-ImageRef(1,0) && scores[i-1] > score)*/
		if(corners[i-1].x == pos.x-1 && corners[i-1].y == pos.y && scores[i-1] > score)
			continue;

		/*Check right*/
		/*if(corners[i+1] == pos+ImageRef(1,0) && scores[i+1] > score)*/
		if(corners[i+1].x == pos.x+1 && corners[i+1].y == pos.y && scores[i-1] > score)
			continue;

		/*Check above*/
		if(pos.y != 0 && row_start[pos.y - 1] != -1) 
		{
			if(corners[point_above].y < pos.y - 1)
				point_above = row_start[pos.y-1];

			/*Make point above point to the first of the pixels above the current point,*/
			/*if it exists.*/
			for(; corners[point_above].y < pos.y && corners[point_above].x < pos.x - 1; point_above++);


			for(j=point_above; corners[j].y < pos.y && corners[j].x <= pos.x + 1; j++)
			{
				int x = corners[j].x;
				if( (x == pos.x - 1 || x ==pos.x || x == pos.x+1) && scores[j] > score)
				{
					goto cont;
				}
			}

		}

		/*Check below*/
		if(pos.y != ysize-1 && row_start[pos.y + 1] != -1) /*Nothing below*/
		{
			if(corners[point_below].y < pos.y + 1)
				point_below = row_start[pos.y+1];

			/* Make point below point to one of the pixels belowthe current point, if it*/
			/* exists.*/
			for(; corners[point_below].y == pos.y+1 && corners[point_below].x < pos.x - 1; point_below++);

			for(j=point_below; corners[j].y == pos.y+1 && corners[j].x <= pos.x + 1; j++)
			{
				int x = corners[j].x;
				if( (x == pos.x - 1 || x ==pos.x || x == pos.x+1) && scores[j] > score)
				{
					goto cont;
				}
			}
		}
		

		nonmax_corners[num_nonmax].x = corners[i].x;
		nonmax_corners[num_nonmax].y = corners[i].y;

		num_nonmax++;

		cont:
		;
	}

	*numnx = num_nonmax;

	free(row_start);
	free(scores);
	return nonmax_corners;
}
