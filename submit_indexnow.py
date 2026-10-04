"""Verify the live key and submit sitemap URLs; receipt does not guarantee indexing."""
import json,subprocess,xml.etree.ElementTree as ET,pathlib,re,tempfile
P=pathlib.Path(__file__).parent
key=re.search(r"INDEXNOW_KEY='([^']+)'",(P/'build_directory.py').read_text()).group(1)
host='shorttermrentalvendors.com';origin='https://'+host
key_result=subprocess.run(['curl','-fsS','--max-time','30',origin+'/'+key+'.txt'],capture_output=True,text=True,check=True)
if key_result.stdout.strip()!=key:raise SystemExit('The production ownership file does not match. Submission stopped.')
urls=[e.text for e in ET.parse(P/'dist/sitemap.xml').iter() if e.tag.endswith('loc')]
for start in range(0,len(urls),10000):
 batch=urls[start:start+10000]
 body=json.dumps(dict(host=host,key=key,keyLocation=origin+'/'+key+'.txt',urlList=batch))
 result=subprocess.run(['curl','-sS','--max-time','45','-X','POST','-H','Content-Type: application/json','--data-binary','@-','-w','\n%{http_code}','https://api.indexnow.org/indexnow'],input=body,capture_output=True,text=True,check=True)
 status=int(result.stdout.rsplit('\n',1)[-1]);print(json.dumps({'status':status,'submitted_urls':len(batch),'validation_pending':status==202}))
 if status not in [200,202]:raise SystemExit('IndexNow did not accept the request.')
