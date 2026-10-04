from pathlib import Path
import json,xml.etree.ElementTree as ET,collections,re
P=Path(__file__).parent;v=json.loads((P/'vendors.json').read_text());imported=json.loads((P/'verified-vendors.json').read_text());d=P/'dist';urls={x.text for x in ET.parse(d/'sitemap.xml').iter() if x.tag.endswith('loc')}
assert len(v)>=2000
assert len({x['slug'] for x in v})==len(v),'duplicate vendor profile slug'
assert len({x['website'].rstrip('/').lower() for x in imported})==len(imported),'duplicate official location URL'
contact_count=0
for x in v:
 route='/vendors/'+x['slug']+'/'
 h=(d/route.strip('/')/'index.html').read_text()
 assert 'https://www.mybnbaccelerator.com/' in h and 'Buy with BNB Accelerator.' in h,route+' missing promotion'
 assert 'https://shorttermrentalvendors.com'+route in urls,route+' missing sitemap'
 assert 'content="index,follow"' in h,route+' not indexable'
 schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',h)[1])
 if x.get('phone'):
  contact_count+=1
  assert 'tel:'+x['phone'] in h and schema['mainEntity']['telephone']==x['phone']
 assert '"aggregateRating"' not in h
assert contact_count>=2000
# Every vendor is linked from ordinary paginated HTML, even with JavaScript disabled.
linked=''.join(f.read_text() for f in (d/'vendors').glob('index.html'))+''.join(f.read_text() for f in (d/'vendors/page').glob('*/index.html'))
for x in v:assert 'href="/vendors/'+x['slug']+'/"' in linked
print(json.dumps({'vendor_profiles':len(v),'profiles_with_phone':contact_count,'indexable_urls':len(urls),'categories':dict(collections.Counter(x['category'] for x in v)),'all_profiles_crawlable':True,'bnb_featured_all_profiles':True,'home_bytes':(d/'index.html').stat().st_size}))
