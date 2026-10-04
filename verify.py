from pathlib import Path
from html.parser import HTMLParser
import json,xml.etree.ElementTree as ET
p=Path(__file__).parent;d=p/'dist';errors=[];count=0
class Inspect(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.h1=0;self.robot=None
 def handle_starttag(self,t,a):
  x=dict(a)
  if t=='a':self.links.append(x.get('href',''))
  if t=='h1':self.h1+=1
  if t=='meta' and x.get('name')=='robots':self.robot=x.get('content')
for f in d.rglob('index.html'):
 count+=1;h=Inspect();h.feed(f.read_text())
 if h.h1!=1:errors.append(str(f)+' h1')
 for l in h.links:
  if l.startswith('/') and not (d/l.strip('/')/'index.html').exists():errors.append(str(f)+' missing '+l)
for e in ET.parse(d/'sitemap.xml').getroot():
 url=e[0].text;route='/'+'/'.join(url.split('/')[3:]);f=d/route.strip('/')/'index.html';h=Inspect();h.feed(f.read_text())
 if h.robot!='index,follow':errors.append('sitemap contains noindex '+route)
assert not errors,errors[:20]
assert not list((d/'markets/colorado').glob('**/index.html'))
assert all(v['state']!='Colorado' for v in json.loads((p/'vendors.json').read_text()))
print(json.dumps({'html_pages_checked':count,'broken_internal_links':len(errors),'sitemap_valid':True,'colorado_excluded':True}))
