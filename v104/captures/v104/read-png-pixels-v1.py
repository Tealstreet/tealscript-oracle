import hashlib
import struct
import zlib
from pathlib import Path


def decode(path):
    raw=Path(path).read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n'
    offset=8;chunks=[];compressed=[];profile=[]
    while offset<len(raw):
        size=struct.unpack('>I',raw[offset:offset+4])[0];kind=raw[offset+4:offset+8]
        data=raw[offset+8:offset+8+size];crc=struct.unpack('>I',raw[offset+8+size:offset+12+size])[0]
        assert zlib.crc32(kind+data)&0xffffffff==crc
        chunks.append(dict(type=kind.decode(),bytes=size,sha256=hashlib.sha256(data).hexdigest()))
        if kind==b'IHDR':width,height,depth,color,compression,filtering,interlace=struct.unpack('>IIBBBBB',data)
        elif kind==b'IDAT':compressed.append(data)
        elif kind in [b'iCCP',b'sRGB',b'gAMA',b'cHRM']:
            record=dict(type=kind.decode(),rawHex=data.hex())
            if kind==b'iCCP':
                name,encoded=data.split(b'\0',1);assert encoded[0]==0
                icc=zlib.decompress(encoded[1:]);record.update(name=name.decode('latin1'),decodedBytes=len(icc),decodedSha256=hashlib.sha256(icc).hexdigest())
            profile.append(record)
        offset+=12+size
    assert offset==len(raw) and chunks[-1]['type']=='IEND'
    assert depth==8 and color in [2,6] and compression==filtering==interlace==0
    channels=3 if color==2 else 4;stride=width*channels
    scan=zlib.decompress(b''.join(compressed));assert len(scan)==height*(stride+1)
    previous=bytearray(stride);rows=[]
    def paeth(a,b,c):
        p=a+b-c;da,db,dc=abs(p-a),abs(p-b),abs(p-c)
        return a if da<=db and da<=dc else b if db<=dc else c
    for y in range(height):
        start=y*(stride+1);mode=scan[start];assert 0<=mode<=4
        row=bytearray(scan[start+1:start+1+stride])
        for x in range(stride):
            left=row[x-channels] if x>=channels else 0;up=previous[x];corner=previous[x-channels] if x>=channels else 0
            predictor=[0,left,up,(left+up)//2,paeth(left,up,corner)][mode]
            row[x]=(row[x]+predictor)&255
        rows.append(bytes(row));previous=row
    def pixel(x,y):
        assert 0<=x<width and 0<=y<height
        return list(rows[y][x*channels:(x+1)*channels])
    return dict(width=width,height=height,channels=channels,bitDepth=depth,colorType=color,chunks=chunks,colorMetadata=profile,pixel=pixel,rawSha256=hashlib.sha256(raw).hexdigest(),policy='Lossless PNG sample decoding only; no ICC transform, resampling, editing or inferred display color space')


def rle(points):
    result=[]
    for coordinate,value in points:
        if result and result[-1]['last']+1==coordinate and result[-1]['sample']==value:result[-1]['last']=coordinate
        else:result.append(dict(first=coordinate,last=coordinate,sample=value))
    return result
