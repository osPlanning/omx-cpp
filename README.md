
The C++ API does more than the simple example below.  Refer to the header file 
for more information.

```
/* declarations */
OMXMatrix *omxMfs;
double omxDataBuffer[MAXZONES + 1]; //OMX is doubles
char* omxMfsFileName = "mfs.omx";

/* open omx file as read/write */
omxMfs = new OMXMatrix();
if (isOMX(omxMfsFileName)) {
  omxMfs->openFile(omxMfsFileName);
} else {
  printf("error: cannot open OMX mfs file.\n");
}

/* initialize omx data buffer */
for (i = 0; i <= MAXZONES + 1; i++) {
  omxDataBuffer[i] = 0.0;
}

/* read and write a row */
int zones = omxMfs->getRows();
omxMfs->getRow("mf1", 1, &omxDataBuffer);
omxMfs->writeRow("mf1", 1, omxDataBuffer);
```
