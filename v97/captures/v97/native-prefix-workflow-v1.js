
async function capturePrefixSession(asset,label,dir,pageId=9){
 const sessionDir=dir+'/session-'+label+'-v1';
 const guard=await tools.exec_command({cmd:"python3 -c \"from pathlib import Path; p=Path('"+sessionDir+"/session-start-v1.json'); assert not p.exists(); assert len(list(Path('"+dir+"').glob('session-*-v1/session-start-v1.json')))<2\" ",max_output_tokens:300});
 if(guard.exit_code!==0)throw Error(guard.output);
 const startedAtUtc=new Date().toISOString();
 await persist(sessionDir+'/session-start-v1.json',JSON.stringify({source:asset.id,originalSource:asset.originalSourceId,sourceSha256:asset.sha256,frontier:label,startedAtUtc,inputChanges:0},null,2)+'\n');
 await snap(sessionDir+'/before-export-v1.txt',pageId);
 const trigger=await exportNative('chart',sessionDir,pageId);
 const csv=await copyLatestCsv(sessionDir,'chart',trigger);
 const observed=await tools.exec_command({cmd:"python3 v97/captures/v97/inspect-prefix-v1.py '"+csv.path+"'",max_output_tokens:6000});
 if(observed.exit_code!==0)throw Error(observed.output);
 const frontier=JSON.parse(observed.output);
 await persist(sessionDir+'/capture-frontier-inspection-v1.json',JSON.stringify(frontier,null,2)+'\n');
 await snap(sessionDir+'/after-export-v1.txt',pageId);await shot(sessionDir+'/after-export-v1.jpg',pageId);
 const receipt={version:'v1',source:asset.id,originalSource:asset.originalSourceId,sourceSha256:asset.sha256,frontier:label,startedAtUtc,completedAtUtc:new Date().toISOString(),csv,frontierInspection:frontier,nativeContext:'BINANCE:BTCUSDT2m Candles UTC; new layout208236729/euz5a92K',inputChanges:0,sourceChanges:0,sourceSpecificExecutionIdentity:null,actualNativeCalculationSessionId:null,sessionIdentity:label==='initial'?'Initial naturally loaded source frontier':'Separate frontier after the one authorized native calendar action; never stitched to initial CSV'};
 await persist(sessionDir+'/session-receipt-v1.json',JSON.stringify(receipt,null,2)+'\n');
 return receipt;
}
async function captureV97OwnedPrefix(asset,pageId=9){
 const dir='v97/captures/v97/'+asset.id+'/attempt-v1';
 let receipt=null;
 try{
  receipt=await captureV97(asset,pageId,true);
  if(!receipt?.add?.success)return receipt;
  await inspectV97Runtime(dir,pageId);
  receipt.sessions.push(await capturePrefixSession(asset,'initial',dir,pageId));
  const first=receipt.sessions[0].frontierInspection;
  if(!first.preliminaryContiguousOwnIndexZeroCandidate){
   const requestedDate=first.observedOwnFirstTimeDateUtc||'2026-09-14';
   const basis={version:'v1',source:asset.id,sourceSha256:asset.sha256,privateId:receipt.privateId,requestedDate,chosenBasis:first.observedOwnFirstTimeDateUtc?'Current exact source own FIRST_TIME in initial original CSV':'Historical navigation hint only; current own FIRST_TIME unavailable',initialCsv:receipt.sessions[0].csv.path,firstFrontierRaw:first.firstFrontierRaw,calendarActionAllowance:1,attemptStartedAtUtc:new Date().toISOString(),noRepeat:true};
   await persist(dir+'/history-navigation-start-v1.json',JSON.stringify(basis,null,2)+'\n');
   await goToDate(requestedDate,dir,pageId);
   await new Promise(r=>setTimeout(r,5000));
   await snap(dir+'/post-navigation-settled-v1.txt',pageId);await shot(dir+'/post-navigation-settled-v1.jpg',pageId);
   receipt.sessions.push(await capturePrefixSession(asset,'post-navigation',dir,pageId));
  }
  await removeOwnStudy(receipt.studyTitle,dir,pageId);receipt.removed=true;
  receipt.status='NATIVE CAPTURES RETAINED; OWN PREFIX AND PROPERTY AUDIT PENDING';
  receipt.calendarSelections=receipt.sessions.length===2?1:0;receipt.completedAtUtc=new Date().toISOString();
  await persist(dir+'/capture-receipt-v1.json',JSON.stringify(receipt,null,2)+'\n');
  store('v97Attached',receipt);
  text({source:asset.id,status:receipt.status,sessions:receipt.sessions.length,calendarSelections:receipt.calendarSelections,finalPreliminaryOwnZeroCandidate:receipt.sessions.at(-1).frontierInspection.preliminaryContiguousOwnIndexZeroCandidate,rows:receipt.sessions.at(-1).csv.rows,removed:receipt.removed});
  return receipt;
 }catch(error){
  await snap(dir+'/prefix-partial-v1.txt',pageId);await shot(dir+'/prefix-partial-v1.jpg',pageId);
  await persist(dir+'/prefix-partial-v1.json',JSON.stringify({source:asset.id,error:String(error),atUtc:new Date().toISOString(),receipt,sourceRetryAllowed:false,calendarRetryAllowed:false},null,2)+'\n');
  throw error;
 }
}
