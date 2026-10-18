async function verifyNativeEditor(asset,dir,pageId,prefix='full-editor-ranges'){
 const lines=asset.source.split('\n');
 const starts=[0];for(let i=0;i<lines.length-1;i++)starts.push(starts.at(-1)+lines[i].length+1);
 plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'Escape'}));
 plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'ArrowLeft'}));
 plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'Meta+ArrowUp'}));
 const initial=await snap(dir+'/'+prefix+'-start-v1.txt',pageId);
 if(!/button "Line 1, Col 1"/.test(initial))throw Error('Native full-editor range inspection did not begin at document start');
 let currentLine=1;const covered=Array(asset.source.length).fill(false),assembled=Array(asset.source.length),records=[];
 while(currentLine<lines.length){
  const endLine=Math.min(lines.length,currentLine+2);
  for(let i=currentLine;i<endLine;i++)plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'Shift+ArrowDown'}));
  const filename=prefix+'-'+currentLine+'-'+endLine+'-v1.txt';
  const snapshot=await snap(dir+'/'+filename,pageId);
  const cursor=snapshot.match(/button "Line (\d+), Col (\d+)"/);
  if(!cursor||Number(cursor[1])!==endLine||Number(cursor[2])!==1)throw Error('Native selected-range cursor boundary differs; no source repair/retry');
  const value=snapshot.match(/roledescription="editor" value="([\s\S]*?)"\n\s+uid=/)?.[1];
  if(value===undefined||value.length===0)throw Error('Native selected-range text unavailable');
  const valueFile=prefix+'-'+currentLine+'-'+endLine+'-exposed-v1.pine';await persist(dir+'/'+valueFile,value);
  const from=starts[currentLine-1],to=starts[endLine-1],matches=[];
  for(let at=asset.source.indexOf(value);at!==-1;at=asset.source.indexOf(value,at+1))if(at<=from&&at+value.length>=to)matches.push(at);
  if(matches.length!==1)throw Error('Native range is abbreviated, mismatched or ambiguous; no source repair/retry');
  const at=matches[0];for(let i=0;i<value.length;i++){if(covered[at+i]&&assembled[at+i]!==value[i])throw Error('Native overlapping ranges contradict');covered[at+i]=true;assembled[at+i]=value[i];}
  records.push({nativeSnapshot:filename,nativeUiText:valueFile,selectionStartLine:currentLine,selectionEndLine:endLine,selectionColumns:[1,1],exposedCharacterRange:[at,at+value.length],selectionCharacterRange:[from,to],uniqueExactRequestedRange:true});
  plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'ArrowRight'}));currentLine=endLine;
 }
 if(covered.some(v=>!v)||assembled.join('')!==asset.source)throw Error('Native full-editor ranges do not cover every requested character before Save');
 await persist(dir+'/'+prefix+'-assembled-v1.pine',assembled.join(''));
 const receipt={version:'v1',requestedSourceSha256:asset.sha256,sourceId:asset.id,exact:true,beforeSave:true,method:'Native keyboard bounded selections and accessibility text; every requested character independently covered by exact overlapping exposed ranges',rangeSnapshots:records,coveredCharacters:covered.length,sourceRepairOrRetry:false,hiddenInspection:false};
 await persist(dir+'/'+prefix+'-verification-v1.json',JSON.stringify(receipt,null,2)+'\n');return receipt;
}
