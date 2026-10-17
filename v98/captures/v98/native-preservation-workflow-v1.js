
const f=new Function('tools','text','store','load',load('v98helpers')+"\nreturn {snap,shot,plain,uidFor,latest,persist};")(tools,text,store,load);
let s=await f.snap('v98/captures/v98/environment-v2/new-layout-before-save-v1.txt',10);
const save=s.match(/uid=(\S+) button "Save all charts for all symbols and intervals on your layout"/);
if(save){f.plain(await tools.mcp__chrome_devtools__click({pageId:10,uid:save[1]}));await new Promise(r=>setTimeout(r,500));}
else if(!s.includes('button "All changes saved" disableable disabled'))throw Error('New-layout Save control unavailable');
await f.snap('v98/captures/v98/environment-v2/new-layout-clean-saved-v1.txt',10);
await f.shot('v98/captures/v98/environment-v2/new-layout-clean-saved-v1.jpg',10);
let net=f.plain(await tools.mcp__chrome_devtools__list_network_requests({pageId:10,resourceTypes:['fetch','xhr']}));
const saves=net.split('\n').filter(l=>l.includes('POST https://www.tradingview.com/api/v1/charts/save/ [200]'));
if(save&&!saves.length)throw Error('New-layout Save response unavailable');
const bodyBase='/var/folders/n9/zs28sr2d00jbkxrn9n_g5p3h0000gn/T/oracle-v98-preservation';
if(saves.length){
 const reqid=Number(saves.at(-1).match(/reqid=(\d+)/)[1]);
 f.plain(await tools.mcp__chrome_devtools__get_network_request({pageId:10,reqid,responseFilePath:bodyBase+'-save.network-response'}));
 await f.persist('v98/captures/v98/environment-v2/native-layout-save-receipt-v1.json',JSON.stringify({requestId:reqid,pageId:10,atUtc:new Date().toISOString(),onlyNewLayout:true},null,2)+'\n');
}
s=await f.latest(10);f.plain(await tools.mcp__chrome_devtools__click({pageId:10,uid:f.uidFor(s,/uid=(\S+) button "Manage layouts"/)}));
s=await f.latest(10);f.plain(await tools.mcp__chrome_devtools__click({pageId:10,uid:f.uidFor(s,/uid=(\S+) row "Open layout"/)}));
await f.snap('v98/captures/v98/environment-v2/native-layout-dialog-after-v1.txt',10);
net=f.plain(await tools.mcp__chrome_devtools__list_network_requests({pageId:10,resourceTypes:['fetch','xhr']}));
const lists=net.split('\n').filter(l=>l.includes('GET https://www.tradingview.com/my-charts/ [200]'));
if(!lists.length)throw Error('Full saved-layout list not exposed');
const listReqid=Number(lists.at(-1).match(/reqid=(\d+)/)[1]);
f.plain(await tools.mcp__chrome_devtools__get_network_request({pageId:10,reqid:listReqid,responseFilePath:bodyBase+'-list.network-response'}));
await f.persist('v98/captures/v98/environment-v2/native-layout-list-receipt-v1.json',JSON.stringify({requestId:listReqid,pageId:10,atUtc:new Date().toISOString(),method:'Native Manage layouts > Open layout; no old layout selected'},null,2)+'\n');
f.plain(await tools.mcp__chrome_devtools__press_key({pageId:10,key:'Escape'}));
for(let page=1;page<=9;page++)await f.snap('v98/captures/v98/environment-v2/page-'+page+'-after-v1.txt',page);
const r=await tools.exec_command({cmd:"python3 - <<'PY'\nfrom pathlib import Path\nimport json\nb=Path('v98/captures/v98/environment-v2');base=Path('/var/folders/n9/zs28sr2d00jbkxrn9n_g5p3h0000gn/T/oracle-v98-preservation');p=Path(str(base)+'-list.network-response');raw=p.read_bytes();assert len(json.loads(raw))==14;(b/'native-layout-list-after-response-v1.json').write_bytes(raw);p=Path(str(base)+'-save.network-response');(b/'native-layout-save-response-v1.json').write_bytes(p.read_bytes()) if p.exists() else None\nPY",max_output_tokens:1000});
if(r.exit_code)throw Error(r.output);text({preservationNativeEvidence:'CAPTURED',oldSavedRecords:13,oldOpenTabs:9});
