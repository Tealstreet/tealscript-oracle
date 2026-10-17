
const f=new Function('tools','text','store','load',load('v101helpers')+"\nreturn {snap,shot,plain,uidFor,latest,persist};")(tools,text,store,load);
let s=await f.snap('v101/captures/v101/environment-v2/new-layout-before-save-v1.txt',13);
const save=s.match(/uid=(\S+) button "Save all charts for all symbols and intervals on your layout"/);
if(save){f.plain(await tools.mcp__chrome_devtools__click({pageId:13,uid:save[1]}));await new Promise(r=>setTimeout(r,500));}
else if(!s.includes('button "All changes saved" disableable disabled'))throw Error('New-layout Save control unavailable');
await f.snap('v101/captures/v101/environment-v2/new-layout-clean-saved-v1.txt',13);
await f.shot('v101/captures/v101/environment-v2/new-layout-clean-saved-v1.jpg',13);
let net=f.plain(await tools.mcp__chrome_devtools__list_network_requests({pageId:13,resourceTypes:['fetch','xhr']}));
const saves=net.split('\n').filter(l=>l.includes('POST https://www.tradingview.com/api/v1/charts/save/ [200]'));
if(save&&!saves.length)throw Error('New-layout Save response unavailable');
const bodyBase='/var/folders/n9/zs28sr2d00jbkxrn9n_g5p3h0000gn/T/oracle-v101-preservation';
if(saves.length){
 const reqid=Number(saves.at(-1).match(/reqid=(\d+)/)[1]);
 f.plain(await tools.mcp__chrome_devtools__get_network_request({pageId:13,reqid,responseFilePath:bodyBase+'-save.network-response'}));
 await f.persist('v101/captures/v101/environment-v2/native-layout-save-receipt-v1.json',JSON.stringify({requestId:reqid,pageId:13,atUtc:new Date().toISOString(),onlyNewLayout:true},null,2)+'\n');
}
s=await f.latest(12);f.plain(await tools.mcp__chrome_devtools__click({pageId:13,uid:f.uidFor(s,/uid=(\S+) button "Manage layouts"/)}));
s=await f.latest(12);f.plain(await tools.mcp__chrome_devtools__click({pageId:13,uid:f.uidFor(s,/uid=(\S+) row "Open layout"/)}));
await f.snap('v101/captures/v101/environment-v2/native-layout-dialog-after-v1.txt',13);
net=f.plain(await tools.mcp__chrome_devtools__list_network_requests({pageId:13,resourceTypes:['fetch','xhr']}));
const lists=net.split('\n').filter(l=>l.includes('GET https://www.tradingview.com/my-charts/ [200]'));
if(!lists.length)throw Error('Full saved-layout list not exposed');
const listReqid=Number(lists.at(-1).match(/reqid=(\d+)/)[1]);
f.plain(await tools.mcp__chrome_devtools__get_network_request({pageId:13,reqid:listReqid,responseFilePath:bodyBase+'-list.network-response'}));
await f.persist('v101/captures/v101/environment-v2/native-layout-list-receipt-v1.json',JSON.stringify({requestId:listReqid,pageId:13,atUtc:new Date().toISOString(),method:'Native Manage layouts > Open layout; no old layout selected'},null,2)+'\n');
f.plain(await tools.mcp__chrome_devtools__press_key({pageId:13,key:'Escape'}));
const map={1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12};
await f.persist('v101/captures/v101/environment-v2/page-id-mapping-v1.json',JSON.stringify({version:'v1',basis:'Native list_pages at v101 baseline; stable layout URL mapping with unchanged page IDs',originalToCurrentPageId:map,newLayoutPageId:13},null,2)+'\n');
for(let page=1;page<=12;page++)await f.snap('v101/captures/v101/environment-v2/page-'+page+'-after-v1.txt',map[page]);
const r=await tools.exec_command({cmd:"python3 - <<'PY'\nfrom pathlib import Path\nimport json\nb=Path('v101/captures/v101/environment-v2');base=Path('/var/folders/n9/zs28sr2d00jbkxrn9n_g5p3h0000gn/T/oracle-v101-preservation');p=Path(str(base)+'-list.network-response');raw=p.read_bytes();assert len(json.loads(raw))==17;(b/'native-layout-list-after-response-v1.json').write_bytes(raw);p=Path(str(base)+'-save.network-response');(b/'native-layout-save-response-v1.json').write_bytes(p.read_bytes()) if p.exists() else None\nPY",max_output_tokens:1000});
if(r.exit_code)throw Error(r.output);text({preservationNativeEvidence:'CAPTURED',oldSavedRecords:16,oldOpenTabs:12});
