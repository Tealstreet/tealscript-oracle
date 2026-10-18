
function plain(r){if(r.isError)throw new Error(r.content?.filter(c=>c.type==='text').map(c=>c.text).join('\n'));return r.content?.filter(c=>c.type==='text').map(c=>c.text).join('\n')||'';}
async function persist(path,data,base64=false){const payload=JSON.stringify({path,data,base64});const r=await tools.exec_command({cmd:"python3 -c 'import sys,json,pathlib,base64; d=json.load(sys.stdin); p=pathlib.Path(d[\"path\"]); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(base64.b64decode(d[\"data\"]) if d[\"base64\"] else d[\"data\"].encode())' <<'ORACLE_PAYLOAD'\n"+payload+"\nORACLE_PAYLOAD",workdir:"/Users/samuelsteady/cs/tealscript-oracle",max_output_tokens:1000});if(r.exit_code!==0)throw new Error(r.output);}
async function persistResult(path,r){await persist(path,JSON.stringify(r,null,2)+'\n');}
async function shot(path,pageId){const r=await tools.mcp__chrome_devtools__take_screenshot({pageId,format:'jpeg',quality:85});plain(r);const img=r.content.find(c=>c.type==='image');if(!img)throw new Error('No native screenshot image');await persist(path,img.data,true);}
async function snap(path,pageId){const r=await tools.mcp__chrome_devtools__take_snapshot({pageId});plain(r);await persist(path,plain(r));store('v91LastSnapshot',plain(r));return plain(r);}

async function exportNative(stage,dir,pageId=3){
 let s=plain(await tools.mcp__chrome_devtools__take_snapshot({pageId}));
 let uid=s.match(/uid=(\S+) button "Manage layouts"/)?.[1];if(!uid)throw new Error('Missing native layout menu');
 plain(await tools.mcp__chrome_devtools__click({pageId,uid}));
 s=plain(await tools.mcp__chrome_devtools__take_snapshot({pageId}));
 uid=s.match(/uid=(\S+) row "Download chart data"/)?.[1];if(!uid)throw new Error('Missing export menu');
 plain(await tools.mcp__chrome_devtools__click({pageId,uid}));
 s=await snap(dir+'/'+stage+'-export-dialog-v1.txt',pageId);
 if(!s.includes('Time format (UTC)')||!s.includes('UNIX timestamp'))throw new Error('Unexpected export time format');
 uid=s.match(/uid=(\S+) button "Download"/)?.[1];if(!uid)throw new Error('Missing download button');
 const startedAtUtc=new Date().toISOString();plain(await tools.mcp__chrome_devtools__click({pageId,uid}));
 await persist(dir+'/'+stage+'-export-trigger-v1.json',JSON.stringify({startedAtUtc,completedAtUtc:new Date().toISOString(),stage,method:'Native Manage layouts > Download chart data > Download',sourceIsolated:false},null,2)+'\n');
 await snap(dir+'/'+stage+'-post-export-snapshot-v1.txt',pageId);
 return {startedAtUtc,stage};
}

async function latest(pageId=3){const s=plain(await tools.mcp__chrome_devtools__take_snapshot({pageId}));store('v91LastSnapshot',s);return s;}
function uidFor(s,pattern){const m=s.match(pattern);if(!m)throw new Error('Native element missing '+pattern);return m[1];}
async function newIndicator(pageId=3){let s=await latest(pageId);let uid=uidFor(s,/uid=(\S+) button "(?:v\d+-[^"]+|proposed-v\d+-[^"]+|Untitled script)" expandable/);plain(await tools.mcp__chrome_devtools__click({pageId,uid}));s=await latest(pageId);uid=uidFor(s,/uid=(\S+) menuitem "Create new"/);plain(await tools.mcp__chrome_devtools__click({pageId,uid}));s=await latest(pageId);uid=uidFor(s,/uid=(\S+) menuitem "Indicator"/);plain(await tools.mcp__chrome_devtools__click({pageId,uid}));s=await latest(pageId);return uidFor(s,/uid=(\S+) textbox "Editor content/);}
async function enterExact(source,editorUid,pageId=3){
 plain(await tools.mcp__chrome_devtools__click({pageId,uid:editorUid}));
 for(const key of ['Meta+A','Backspace'])plain(await tools.mcp__chrome_devtools__press_key({pageId,key}));
 const lines=source.split('\n').slice(0,-1);
 for(let i=0;i<lines.length;i++){
  for(const key of ['Escape','Home','Shift+End','Delete'])plain(await tools.mcp__chrome_devtools__press_key({pageId,key}));
  if(lines[i])plain(await tools.mcp__chrome_devtools__type_text({pageId,text:lines[i]}));
  await new Promise(r=>setTimeout(r,1000));
  plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'Escape'}));
  await new Promise(r=>setTimeout(r,150));
  plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'Escape'}));
  plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'End'}));
  await new Promise(r=>setTimeout(r,150));
  plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'Enter'}));
  let m=null;
  for(let check=0;check<10;check++){
   await new Promise(r=>setTimeout(r,150));
   const snapshot=await latest(pageId);m=snapshot.match(/button "Line (\d+), Col (\d+)"/);
   if(m&&Number(m[1])===i+2)break;
  }
  if(!m||Number(m[1])!==i+2)throw new Error('Native cursor line mismatch '+(i+1));
  if(i%10===0)text({nativeSourceLine:i+1,total:lines.length,cursorLine:Number(m[1])});
 }
 return lines.length;
}

async function nativeFiles(reqid,dir,prefix,expectedSource=null,pageId=3){
 const base='/var/folders/n9/zs28sr2d00jbkxrn9n_g5p3h0000gn/T/oracle-v104-'+reqid;
 const args={pageId,reqid,responseFilePath:base+'.network-response'};if(expectedSource)args.requestFilePath=base+'.network-request';
 const r=await tools.mcp__chrome_devtools__get_network_request(args);plain(r);
 const payload=JSON.stringify({reqid,dir,prefix,base,expectedSource,observedAtUtc:new Date().toISOString()});
 const py="import sys,json,pathlib,hashlib\nd=json.load(sys.stdin); p=pathlib.Path(d['dir']);p.mkdir(parents=True,exist_ok=True); b=pathlib.Path(d['base']+'.network-response').read_bytes(); (p/(d['prefix']+'-response-v1.json')).write_bytes(b); r=json.loads(b); out={'requestId':d['reqid'],'observedAtUtc':d['observedAtUtc'],'success':r.get('success'),'responseBytes':len(b),'responseSha256':hashlib.sha256(b).hexdigest(),'nativeMetaInfoId':(r.get('result') or {}).get('metaInfo',{}).get('id'),'sourceBinding':None}\nif d['expectedSource']:\n q=pathlib.Path(d['base']+'.network-request').read_bytes();(p/(d['prefix']+'-request-v1.txt')).write_bytes(q); sep=b'\\r\\n' if b'\\r\\n' in q else b'\\n'; boundary=q.strip().split(sep)[0];src=q.split(sep+sep,1)[1].split(sep+boundary,1)[0]; norm=src.replace(b'\\r\\n',b'\\n');expected=pathlib.Path(d['expectedSource']).read_bytes();(p/'executed-v1.pine').write_bytes(norm);out['sourceBinding']={'expectedSha256':hashlib.sha256(expected).hexdigest(),'executedSha256':hashlib.sha256(norm).hexdigest(),'nativeFormSourceSha256':hashlib.sha256(src).hexdigest(),'nativeFormLineEndingNormalizationOnly':True,'exact':norm==expected}; assert norm==expected\n(p/(d['prefix']+'-transport-v1.json')).write_text(json.dumps(out,indent=2)+'\\n');print(json.dumps(out))";
 const cmd="python3 -c '"+py.replace(/'/g,"'\\''")+"' <<'ORACLE_PAYLOAD'\n"+payload+"\nORACLE_PAYLOAD";
 const result=await tools.exec_command({cmd,max_output_tokens:1800});if(result.exit_code!==0)throw new Error(result.output);text(JSON.parse(result.output));return JSON.parse(result.output);
}

async function waitSnapshot(pattern,pageId=3){for(let i=0;i<15;i++){const s=await latest(pageId);if(pattern.test(s))return s;await new Promise(r=>setTimeout(r,200));}throw new Error('Native UI wait failed '+pattern);}
async function openEditor(pageId=3){let s=await latest(pageId);if(!/textbox "Editor content/.test(s)){plain(await tools.mcp__chrome_devtools__click({pageId,uid:uidFor(s,/uid=(\S+) button "Pine Editor"/)}));s=await waitSnapshot(/textbox "Editor content/,pageId);}return s;}
async function saveNew(name,dir,pageId=3){plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'Meta+S'}));let s=await waitSnapshot(/"New script name"/,pageId);const uid=uidFor(s,/uid=(\S+) textbox focusable focused value=/);plain(await tools.mcp__chrome_devtools__fill({pageId,uid,value:name}));s=await latest(pageId);plain(await tools.mcp__chrome_devtools__click({pageId,uid:uidFor(s,/uid=(\S+) button "Save"\n/)}));await snap(dir+'/post-save-immediate-v1.txt',pageId);for(let i=0;i<20;i++){const r=plain(await tools.mcp__chrome_devtools__list_network_requests({pageId,resourceTypes:['fetch','xhr']}));const lines=r.split('\n').filter(l=>l.includes('/pine-facade/save/new?name='+name)&&l.includes('[200]'));if(lines.length)return Number(lines.at(-1).match(/reqid=(\d+)/)[1]);await new Promise(r=>setTimeout(r,250));}throw new Error('Native Save response unavailable');}
async function closeEditor(pageId=3){let s=await latest(pageId);if(/textbox "Editor content/.test(s)){plain(await tools.mcp__chrome_devtools__click({pageId,uid:uidFor(s,/uid=(\S+) button "Close" description="Close"/)}));}}
async function removeOwnStudy(title,dir,pageId=3){await closeEditor(pageId);let s=await latest(pageId);if(!/tab "Object tree"/.test(s)){plain(await tools.mcp__chrome_devtools__click({pageId,uid:uidFor(s,/uid=(\S+) button "Object tree and data window"/)}));s=await latest(pageId);}plain(await tools.mcp__chrome_devtools__click({pageId,uid:uidFor(s,/uid=(\S+) tab "Object tree"/)}));await new Promise(r=>setTimeout(r,350));s=await latest(pageId);const tree=s.split('tab "Object tree"')[1];const line=tree.split('\n').find(l=>{const m=l.match(/uid=\S+ (?:StaticText )?(\".*\")$/);if(!m)return false;const name=JSON.parse(m[1]);return name===title||name.startsWith(title+' (');});if(!line)throw new Error('Own study not found in native tree '+title);plain(await tools.mcp__chrome_devtools__click({pageId,uid:line.match(/uid=(\S+)/)[1]}));plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'Delete'}));await new Promise(r=>setTimeout(r,350));s=await snap(dir+'/post-remove-v1.txt',pageId);const treeAfter=s.split('tab "Object tree"')[1]?.split('generic "Trading panel"')[0]||'';if(treeAfter.includes(JSON.stringify(title)))throw new Error('Own study remains attached');return s;}

async function copyLatestCsv(dir,stem,trigger){const payload=JSON.stringify({dir,stem,trigger});const py="import sys,json,pathlib,csv,hashlib,time\nd=json.load(sys.stdin); fs=sorted((pathlib.Path.home()/'Downloads').glob('BINANCE_BTCUSDT, *.csv'),key=lambda p:p.stat().st_mtime);p=fs[-1];b=p.read_bytes();out=pathlib.Path(d['dir']);target=out/(d['stem']+'-native-v1.csv');target.write_bytes(b);rows=list(csv.reader(b.decode('utf-8-sig').splitlines()));m={'originalDownloadName':p.name,'downloadModifiedAtEpoch':p.stat().st_mtime,'exportTrigger':d['trigger'],'path':str(target),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'rows':len(rows)-1,'headers':rows[0],'firstRawRow':rows[1],'lastRawRow':rows[-1]};(out/(d['stem']+'-download-v1.json')).write_text(json.dumps(m,indent=2)+'\\n');print(json.dumps({'path':str(target),'rows':len(rows)-1,'columns':len(rows[0]),'firstTimeRaw':rows[1][0],'lastTimeRaw':rows[-1][0]}))";
 const r=await tools.exec_command({cmd:"python3 -c '"+py.replace(/'/g,"'\\''")+"' <<'ORACLE_PAYLOAD'\n"+payload+"\nORACLE_PAYLOAD",max_output_tokens:1500});if(r.exit_code!==0)throw new Error(r.output);text(JSON.parse(r.output));return JSON.parse(r.output);}
async function pngShot(path,pageId=5){const r=await tools.mcp__chrome_devtools__take_screenshot({pageId,format:'png'});plain(r);const img=r.content.find(c=>c.type==='image');if(!img)throw Error('No native PNG');await persist(path,img.data,true);}
async function captureV104(asset,pageId=5,holdBeforeDefaultSession=false){
 const dir='v104/captures/v104/'+asset.id+'/attempt-v1';
 const guard=await tools.exec_command({cmd:"python3 -c \"from pathlib import Path; p=Path('"+dir+"/attempt-start-v1.json'); assert not p.exists(), 'Source attempt already consumed'; assert len(list(Path('v104/captures/v104').glob('*/attempt-v1/attempt-start-v1.json')))<13, 'Source budget exhausted'\"",max_output_tokens:300});
 if(guard.exit_code!==0)throw Error(guard.output);
 await persist(dir+'/attempt-start-v1.json',JSON.stringify({nativeEntryTooling:'v104/captures/v104/native-workflow-v1.js',nativeEntryPolicy:'Single Enter per line with settling/Escape/End and cursor guard; full editor verified through two-line native selections before Save; no source repair or retry',id:asset.id,sourcePath:'v104/'+asset.path,sourceSha256:asset.sha256,startedAtUtc:new Date().toISOString(),saveLimit:1,addLimit:1,inputStates:asset.inputStates},null,2)+'\n');
 await snap(dir+'/context-before-v1.txt',pageId);
 let sourceEntered=false,save=null,add=null;
 try{
  await openEditor(pageId);const editor=await newIndicator(pageId);await enterExact(asset.source,editor,pageId);
  await verifyNativeEditor(asset,dir,pageId);
  await persist(dir+'/full-editor-range-clock-v1.json',JSON.stringify({completedBeforeSaveAtUtc:new Date().toISOString()},null,2)+'\n');
  sourceEntered=true;
  const req=await saveNew(asset.privateSaveName||asset.id+'-attempt-v1',dir,pageId);
  save=await nativeFiles(req,dir,'save','v104/'+asset.path,pageId);
  await snap(dir+'/post-save-settled-v1.txt',pageId);await shot(dir+'/post-save-settled-v1.jpg',pageId);
  if(!save.success){
   await persist(dir+'/capture-receipt-v1.json',JSON.stringify({id:asset.id,sourceSha256:asset.sha256,status:'NATIVE SAVE COMPILER REFUSAL',save,add:null,sourceEntered,completedAtUtc:new Date().toISOString(),sourceExact:true,studyAdded:false,markers:null,markerStatus:'UNOBSERVED; native raw UI/body evidence retained'},null,2)+'\n');
   await closeEditor(pageId);text({source:asset.id,status:'NATIVE SAVE COMPILER REFUSAL',saveRequest:req});return {id:asset.id,status:'REFUSAL'};
  }
  let s=await snap(dir+'/pre-add-v1.txt',pageId);await shot(dir+'/pre-add-v1.jpg',pageId);
  const addedAtUtc=new Date().toISOString();plain(await tools.mcp__chrome_devtools__click({pageId,uid:uidFor(s,/uid=(\S+) button "Add to chart"/)}));
  await persist(dir+'/add-trigger-v1.json',JSON.stringify({addedAtUtc},null,2)+'\n');await snap(dir+'/post-add-immediate-v1.txt',pageId);
  const privateId=save.nativeMetaInfoId.replace(/^Script\$/,'').split('@')[0];let addId=null;
  for(let i=0;i<20;i++){const n=plain(await tools.mcp__chrome_devtools__list_network_requests({pageId,resourceTypes:['fetch','xhr']}));const ls=n.split('\n').filter(l=>l.includes('/pine-facade/translate/'+encodeURIComponent(privateId)+'/')&&/\[(200|304)\]/.test(l));if(ls.length){addId=Number(ls.at(-1).match(/reqid=(\d+)/)[1]);break;}await new Promise(r=>setTimeout(r,250));}
  if(!addId)throw Error('Native Add body not found for '+privateId);
  add=await nativeFiles(addId,dir,'add',null,pageId);await snap(dir+'/post-add-settled-v1.txt',pageId);await closeEditor(pageId);
  const title=asset.source.match(/indicator\("([^"]+)"/)?.[1];
  const receipt={id:asset.id,sourceSha256:asset.sha256,sourceExact:true,save,add,privateId,privateVersion:'1.0',studyTitle:title,addedAtUtc,sourceEntered,studyAdded:true,removed:false,markers:null,markerStatus:'UNOBSERVED; raw immediate/settled UI/body retained',sessions:[]};
  store('v104Attached',receipt);
  if(!add.success){await shot(dir+'/add-refusal-v1.jpg',pageId);await persist(dir+'/capture-receipt-v1.json',JSON.stringify({...receipt,status:'NATIVE ADD REFUSAL'},null,2)+'\n');text({source:asset.id,status:'NATIVE ADD REFUSAL'});return receipt;}
  await new Promise(r=>setTimeout(r,3500));
  if(holdBeforeDefaultSession){
   receipt.status='ATTACHED; SINGLE UNCHANGED OBSERVER WINDOW PENDING';
   await persist(dir+'/attach-receipt-v1.json',JSON.stringify(receipt,null,2)+'\n');
   store('v104Attached',receipt);text({source:asset.id,status:receipt.status});return receipt;
  }
  await inspectV104Runtime(dir,pageId);
  receipt.sessions.push(await captureV104Session(asset,0,dir,pageId));
  if(asset.sessionCount===1){await removeOwnStudy(title,dir,pageId);receipt.removed=true;}
  receipt.status=asset.sessionCount===1?'CAPTURED':'DEFAULT CAPTURED; PRESCRIBED INPUT STATES PENDING';receipt.completedAtUtc=new Date().toISOString();
  await persist(dir+'/capture-receipt-v1.json',JSON.stringify(receipt,null,2)+'\n');store('v104Attached',receipt);
  text({source:asset.id,status:receipt.status,save:req,add:addId,sessions:receipt.sessions.length,removed:receipt.removed});return receipt;
 }catch(error){
  await snap(dir+'/partial-attempt-v1.txt',pageId);await shot(dir+'/partial-attempt-v1.jpg',pageId);
  await persist(dir+'/partial-attempt-v1.json',JSON.stringify({id:asset.id,sourceEntered,save,add,error:String(error),atUtc:new Date().toISOString(),retryAllowed:false},null,2)+'\n');
  throw error;
 }
}
async function captureV104Session(asset,mode,dir,pageId=5){
 const sessionDir=dir+'/session-mode'+mode+'-v1';
 await snap(sessionDir+'/before-export-v1.txt',pageId);
 const startedAtUtc=new Date().toISOString();const trigger=await exportNative('chart',sessionDir,pageId);const csv=await copyLatestCsv(sessionDir,'chart',trigger);
 let s=await latest(pageId);plain(await tools.mcp__chrome_devtools__hover({pageId,uid:uidFor(s,/uid=(\S+) button "Manage layouts"/)}));
 const screenshotAtUtc=new Date().toISOString();await snap(sessionDir+'/render-context-v1.txt',pageId);
 if(asset.requiresRenderingScreenshot)await pngShot(sessionDir+'/render-v1.png',pageId);
 const screenshotCompletedAtUtc=asset.requiresRenderingScreenshot?new Date().toISOString():null;
 const receipt={version:'v1',source:asset.id,sourceSha256:asset.sha256,inputMode:mode,inputName:Object.keys(asset.inputStates)[0]||null,sessionIdentity:'New calculation session for this source/input state; no cross-session continuity implied',startedAtUtc,screenshotAtUtc:asset.requiresRenderingScreenshot?screenshotAtUtc:null,screenshotCompletedAtUtc,nativeFrameAsOfClock:null,nativeFrameAsOfClockStatus:'UNOBSERVED; UTCs bound the native screenshot call, not a provider tick frame',csv,nativeContext:'BINANCE:BTCUSDT2m Candles UTC; new layout208421791/uTUPc84s',viewportActions:[],sourceSpecificExecutionIdentity:null};
 await persist(sessionDir+'/session-receipt-v1.json',JSON.stringify(receipt,null,2)+'\n');return receipt;
}

async function inspectV104Runtime(dir,pageId=7){const s=await snap(dir+'/runtime-inspection-before-v1.txt',pageId);const m=s.match(/uid=(\S+) button "Runtime error: ([^"]+)"/);if(!m)return false;plain(await tools.mcp__chrome_devtools__click({pageId,uid:m[1]}));await new Promise(r=>setTimeout(r,350));await snap(dir+'/runtime-error-expanded-v1.txt',pageId);await shot(dir+'/runtime-error-expanded-v1.jpg',pageId);await persist(dir+'/runtime-ui-observation-v1.json',JSON.stringify({observedAtUtc:new Date().toISOString(),codeLabel:m[2],details:'runtime-error-expanded-v1.txt',sourceRepairs:0,saveAddRepeats:0},null,2)+'\n');plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'Escape'}));return true;}

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
