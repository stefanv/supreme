/**********************************************************************
Reads the feature table from "features.txt", copies the features from 
the second frame to those of the third frame, writes the features to 
"feat2.txt", and writes the new feature table to "ft2.txt".  Then the
eighth feature is overwritten with the fifth feature, and the resulting
table is saved to "ft3.txt".
**********************************************************************/

#include <stdio.h>
#include "klt.h"

#ifdef WIN32
int RunExample4()
#else
int main()
#endif
{
  KLT_FeatureList fl;
  KLT_FeatureHistory fh;
  KLT_FeatureTable ft;
  int i;

  ft = KLTReadFeatureTable(NULL, "features.txt");
  fl = KLTCreateFeatureList(ft->nFeatures);
  KLTExtractFeatureList(fl, ft, 1);
  KLTWriteFeatureList(fl, "feat1.txt", "%3d");
  KLTReadFeatureList(fl, "feat1.txt");
  KLTStoreFeatureList(fl, ft, 2);
  KLTWriteFeatureTable(ft, "ft2.txt", "%3d");

  fh = KLTCreateFeatureHistory(ft->nFrames);
  KLTExtractFeatureHistory(fh, ft, 5);

  printf("The feature history of feature number 5:\n\n");
  for (i = 0 ; i < fh->nFrames ; i++)
    printf("%d: (%5.1f,%5.1f) = %d\n",
           i, fh->feature[i]->x, fh->feature[i]->y,
           fh->feature[i]->val);

  KLTStoreFeatureHistory(fh, ft, 8);
  KLTWriteFeatureTable(ft, "ft3.txt", "%6.1f");

  return 0;
}

