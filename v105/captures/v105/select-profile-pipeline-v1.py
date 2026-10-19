import hashlib
import json
import runpy
import struct
import subprocess
import zlib
from datetime import datetime,timezone
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put=HELPERS['ref'],HELPERS['put']


def select():
    directory=BASE/'v105-alpha-composite-v6';png=directory/'attempt-v1/session-mode0-v1/render-v1.png';raw=png.read_bytes()
    assert raw[:8]==b'\x89PNG\r\n\x1a\n';width,height,depth,color,compression,filtering,interlace=struct.unpack('>IIBBBBB',raw[16:29])
    offset=8;chunks=[];profiles=[];causes=[];tags={}
    while offset<len(raw):
        size=struct.unpack('>I',raw[offset:offset+4])[0];kind=raw[offset+4:offset+8];data=raw[offset+8:offset+8+size]
        assert zlib.crc32(kind+data)&0xffffffff==struct.unpack('>I',raw[offset+8+size:offset+12+size])[0]
        name=kind.decode();tags.setdefault(name,[]).append(data)
        if name in ['iCCP','sRGB','gAMA','cHRM','cICP']:
            record=dict(type=name,originalOffsetBytes=offset,payloadBytes=size,payloadSha256=hashlib.sha256(data).hexdigest(),wholeChunkHex=raw[offset:offset+size+12].hex(),payloadHex=data.hex())
            if name=='iCCP':
                label,encoded=data.split(b'\0',1);assert encoded[0]==0
                icc=zlib.decompress(encoded[1:]);path=directory/('original-embedded-profile-'+str(len(profiles)+1)+'-v1.icc')
                if path.exists():assert path.read_bytes()==icc
                else:path.write_bytes(icc)
                profiles.append(path);record.update(profileName=label.decode('latin1'),decodedIcc=ref(path))
            chunks.append(record)
        offset+=12+size
    assert offset==len(raw) and depth==8 and color in [2,6] and compression==filtering==interlace==0
    pipeline=None;verification=None
    if len(profiles)==1 and not tags.get('sRGB') and not tags.get('cICP') and not tags.get('gAMA') and not tags.get('cHRM'):
        icc=profiles[0].read_bytes();valid=len(icc)>=132 and struct.unpack('>I',icc[:4])[0]==len(icc) and icc[36:40]==b'acsp' and icc[16:20]==b'RGB '
        if valid:
            count=struct.unpack('>I',icc[128:132])[0];valid=132+12*count<=len(icc)
            if valid:
                for i in range(count):
                    kind,at,size=struct.unpack('>4sII',icc[132+12*i:144+12*i]);valid=valid and at>=128 and size>=8 and at+size<=len(icc)
        verified=subprocess.run(['/usr/bin/sips','--verify',str(profiles[0])],text=True,capture_output=True)
        verification=dict(command=['/usr/bin/sips','--verify',str(profiles[0])],exitCode=verified.returncode,stdout=verified.stdout,stderr=verified.stderr,headerAndTagBoundsValid=valid)
        if valid and verified.returncode==0 and not verified.stderr.strip():pipeline='EMBEDDED_ICC_TO_FIXED_SRGB_RELATIVE_NO_BPC'
        else:causes.append('Embedded ICC fails strict RGB header/tag-bounds or ColorSync sips verification')
    elif not profiles and len(tags.get('sRGB',[]))==1 and not tags.get('cICP'):
        valid=len(tags['sRGB'][0])==1 and tags['sRGB'][0][0]<=3
        if tags.get('gAMA'):valid=valid and tags['gAMA']==[struct.pack('>I',45455)]
        if tags.get('cHRM'):valid=valid and tags['cHRM']==[struct.pack('>8I',31270,32900,64000,33000,30000,60000,15000,6000)]
        if valid:pipeline='AUTHENTICATED_SRGB_RAW_ENCODED8'
        else:causes.append('sRGB declaration conflicts with gamma/chromaticity or invalid intent bytes')
    else:causes.append('Missing, multiple, conflicting or ambiguous original color-profile declarations; no alternate pipeline permitted')
    return dict(version='v1',selectedAtUtc=datetime.now(timezone.utc).isoformat(),phase='Original metadata only, before reading/scoring or exposing subject/control sample tuples',originalPng=ref(png),pngContainer=dict(width=width,height=height,bitDepth=depth,colorType=color,channels=3 if color==2 else 4,observedAlphaChannel=color==6,syntheticAlpha=False),originalColorChunks=chunks,profileVerification=verification,selectedPipeline=pipeline,notObservedCauses=causes,preregisteredPipeline=ref(BASE/'environment-v1/profile-pipeline-preregistration-v1.json'),targetProfile=ref(BASE/'environment-v1/comparison-srgb-profile-v1.icc'),conversionTool=ref(BASE/'convert-icc-samples-v1.c'),comparisonSpace='Encoded8-bit sRGB',intent='relative-colorimetric',blackPointCompensation=False,rawPixelTuplesReadForSelection=False,scope='No pipeline fitting, native profile/browser/account action, color tolerance, source change or retroactive v104 conversion')


if __name__=='__main__':
    result=select();put(BASE/'v105-alpha-composite-v6/profile-selection-v1.json',result)
    print(json.dumps(dict(selectedPipeline=result['selectedPipeline'],causes=result['notObservedCauses'],originalChunks=[c['type'] for c in result['originalColorChunks']])))
