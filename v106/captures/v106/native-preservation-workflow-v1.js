const pageId=18;
const base='v106/captures/v106/environment-v2';
const bodyBase='/var/folders/n9/zs28sr2d00jbkxrn9n_g5p3h0000gn/T/oracle-v106-preservation';
const f=new Function('tools','text','store','load',load('v106helpersV1')+'\nreturn {snap,shot,plain,uidFor,latest,persist};')(tools,text,store,load);
let s=await f.snap(base+'/new-layout-before-save-v1.txt',pageId);
const save=s.match(/uid=(\S+) button "Save all charts for all symbols and intervals on your layout"/);
if(save){f.plain(await tools.mcp__chrome_devtools__click({pageId,uid:save[1]}));await new Promise(r=>setTimeout(r,500));}
else if(!s.includes('button "All changes saved" disableable disabled'))throw Error('New layout Save control unavailable');
await f.snap(base+'/new-layout-clean-saved-v1.txt',pageId);
await f.shot(base+'/new-layout-clean-saved-v1.jpg',pageId);
let net=f.plain(await tools.mcp__chrome_devtools__list_network_requests({pageId,resourceTypes:['fetch','xhr']}));
const saves=net.split('\n').filter(l=>l.includes('POST https://www.tradingview.com/api/v1/charts/save/ [200]'));
if(save&&!saves.length)throw Error('New layout Save body unavailable');
if(saves.length){
 const reqid=Number(saves.at(-1).match(/reqid=(\d+)/)[1]);
 f.plain(await tools.mcp__chrome_devtools__get_network_request({pageId,reqid,responseFilePath:bodyBase+'-save.network-response'}));
 await f.persist(base+'/native-layout-save-receipt-v1.json',JSON.stringify({requestId:reqid,pageId,atUtc:new Date().toISOString(),onlyNewLayout:true},null,2)+'\n');
}
s=await f.latest(pageId);f.plain(await tools.mcp__chrome_devtools__click({pageId,uid:f.uidFor(s,/uid=(\S+) button "Manage layouts"/)}));
s=await f.latest(pageId);f.plain(await tools.mcp__chrome_devtools__click({pageId,uid:f.uidFor(s,/uid=(\S+) row "Open layout"/)}));
await f.snap(base+'/native-layout-dialog-after-v1.txt',pageId);
net=f.plain(await tools.mcp__chrome_devtools__list_network_requests({pageId,resourceTypes:['fetch','xhr']}));
const lists=net.split('\n').filter(l=>l.includes('GET https://www.tradingview.com/my-charts/ [200]'));
if(!lists.length)throw Error('Full native saved-layout inventory unavailable');
const reqid=Number(lists.at(-1).match(/reqid=(\d+)/)[1]);
f.plain(await tools.mcp__chrome_devtools__get_network_request({pageId,reqid,responseFilePath:bodyBase+'-list.network-response'}));
await f.persist(base+'/native-layout-list-receipt-v1.json',JSON.stringify({requestId:reqid,pageId,atUtc:new Date().toISOString(),method:'Native Manage layouts > Open layout; no old layout selected'},null,2)+'\n');
f.plain(await tools.mcp__chrome_devtools__press_key({pageId,key:'Escape'}));
await f.persist(base+'/pages-after-v1.json',JSON.stringify(await tools.mcp__chrome_devtools__list_pages({}),null,2)+'\n');
for(let page=1;page<=17;page++)await f.snap(base+'/page-'+page+'-after-v1.txt',page);
const copied=await tools.exec_command({cmd:"python3 - <<'PY'\nfrom pathlib import Path\nimport json\nb=Path('v106/captures/v106/environment-v2');p=Path('/var/folders/n9/zs28sr2d00jbkxrn9n_g5p3h0000gn/T/oracle-v106-preservation');raw=Path(str(p)+'-list.network-response').read_bytes();assert len(json.loads(raw))==22;(b/'native-layout-list-after-response-v1.json').write_bytes(raw);s=Path(str(p)+'-save.network-response');(b/'native-layout-save-response-v1.json').write_bytes(s.read_bytes()) if s.exists() else None\nPY",max_output_tokens:1000});
if(copied.exit_code)throw Error(copied.output);
text({preservationNativeEvidence:'CAPTURED',oldSavedRecords:21,oldOpenTabs:17,newLayoutPageId:pageId});
