#include <ColorSync/ColorSync.h>
#include <CoreFoundation/CoreFoundation.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static ColorSyncProfileRef profile(const char *path) {
    CFURLRef url=CFURLCreateFromFileSystemRepresentation(NULL,(const UInt8 *)path,strlen(path),false);
    CFErrorRef error=NULL;
    ColorSyncProfileRef value=ColorSyncProfileCreateWithURL(url,&error);
    CFRelease(url);
    if(!value || error) { if(error) CFShow(error); exit(2); }
    return value;
}

int main(int argc,char **argv) {
    if(argc!=5) { fprintf(stderr,"usage: convert-icc-samples-v1 input.icc output.icc original-rgb8.bin derived-rgb8.bin\n"); return 2; }
    ColorSyncProfileRef src=profile(argv[1]),dst=profile(argv[2]);
    const void *keys[]={kColorSyncProfile,kColorSyncRenderingIntent,kColorSyncTransformTag,kColorSyncBlackPointCompensation};
    const void *srcValues[]={src,kColorSyncRenderingIntentRelative,kColorSyncTransformDeviceToPCS,kCFBooleanFalse};
    const void *dstValues[]={dst,kColorSyncRenderingIntentRelative,kColorSyncTransformPCSToDevice,kCFBooleanFalse};
    CFDictionaryRef sd=CFDictionaryCreate(NULL,keys,srcValues,4,&kCFTypeDictionaryKeyCallBacks,&kCFTypeDictionaryValueCallBacks);
    CFDictionaryRef dd=CFDictionaryCreate(NULL,keys,dstValues,4,&kCFTypeDictionaryKeyCallBacks,&kCFTypeDictionaryValueCallBacks);
    const void *stages[]={sd,dd};
    CFArrayRef sequence=CFArrayCreate(NULL,stages,2,&kCFTypeArrayCallBacks);
    const void *optionKeys[]={kColorSyncConvertQuality};
    const void *optionValues[]={kColorSyncBestQuality};
    CFDictionaryRef options=CFDictionaryCreate(NULL,optionKeys,optionValues,1,&kCFTypeDictionaryKeyCallBacks,&kCFTypeDictionaryValueCallBacks);
    ColorSyncTransformRef transform=ColorSyncTransformCreate(sequence,options);
    if(!transform) { fprintf(stderr,"ColorSyncTransformCreate failed\n"); return 2; }
    FILE *in=fopen(argv[3],"rb");if(!in) return 2;
    if(fseek(in,0,SEEK_END)) return 2;long size=ftell(in);rewind(in);
    if(size<=0 || size%3) return 2;
    unsigned char *original=malloc(size),*converted=malloc(size);
    if(!original || !converted || fread(original,1,size,in)!=(size_t)size) return 2;
    fclose(in);
    bool ok=ColorSyncTransformConvert(transform,size/3,1,converted,kColorSync8BitInteger,kColorSyncAlphaNone,size,original,kColorSync8BitInteger,kColorSyncAlphaNone,size,NULL);
    if(!ok) { fprintf(stderr,"ColorSyncTransformConvert failed\n"); return 2; }
    FILE *out=fopen(argv[4],"wbx");if(!out || fwrite(converted,1,size,out)!=(size_t)size || fclose(out)) return 2;
    fprintf(stdout,"{\"status\":\"PASS\",\"samples\":%ld,\"bitsPerChannel\":8,\"channels\":3,\"intent\":\"relative-colorimetric\",\"blackPointCompensation\":false,\"quality\":\"best\"}\n",size/3);
    free(original);free(converted);CFRelease(transform);CFRelease(options);CFRelease(sequence);CFRelease(sd);CFRelease(dd);CFRelease(src);CFRelease(dst);
    return 0;
}
