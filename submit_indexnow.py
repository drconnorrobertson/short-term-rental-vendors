import json,urllib.request,xml.etree.ElementTree as ET,pathlib,re
P=pathlib.Path(__file__).parent
s=(P/'build_directory.py').read_text();key=re.search(r"INDEXNOW_KEY='([^']+)'",s).group(1)
host='shorttermrentalvendors.com';origin='https://'+host
actual=urllib.request.urlopen(origin+'/'+key+'.txt',timeout=20).read().decode().strip()
if actual!=key:raise SystemExit('Ownership key is not live on the production domain; submission stopped.')
urls=[e.text for e in ET.parse(P/'dist/sitemap.xml').iter() if e.tag.endswith('loc')]
body=json.dumps(dict(host=host,key=key,keyLocation=origin+'/'+key+'.txt',urlList=urls)).encode()
r=urllib.request.urlopen(urllib.request.Request('https://api.indexnow.org/indexnow',data=body,headers={'Content-Type':'application/json'}),timeout=30)
print(json.dumps({'status':r.status,'submitted_urls':len(urls)}))
