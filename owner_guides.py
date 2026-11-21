"""Render original owner operating guides without changing vendor evidence."""
import json
from html import escape as e
from pathlib import Path

def publish(page, intro, crumb, origin, root):
    guides=json.loads((Path(root)/'owner-guides.json').read_text())
    dates={}
    for g in guides:
        route='/guides/'+g['slug']+'/'
        body=crumb('<a href="/guides/">Owner guides</a> / '+e(g['title']))
        body+=intro(g['title'],g['description'],'Owner operating guide')
        body+='<article class="owner-guide"><p class="meta">AI-assisted website editorial · Published '+e(g['published'])+'</p><p>'+e(g['intro'])+'</p>'
        for s in g['sections']:body+='<section><h2>'+e(s['title'])+'</h2><p>'+e(s['text'])+'</p></section>'
        body+='<section><h2>Prepare the handoff</h2><ul class="list">'+''.join('<li>'+e(x)+'</li>' for x in g['checklist'])+'</ul></section>'
        body+='<section><h2>Source and scope</h2><p><a href="'+e(g['source'],quote=True)+'">'+e(g['sourceLabel'])+'</a>. Source checked '+e(g['modified'])+'. This original operating checklist supports a conversation with the responsible provider; it does not certify a vendor or determine legal, tax, safety or coverage requirements.</p></section>'
        body+='<section><h2>Continue your research</h2><p><a href="/guides/">Explore all owner guides</a> · <a href="/vendors/">Research vendor profiles</a> · <a href="/methodology/">Read the evidence standard</a></p><p>A directory profile is a research starting point. Confirm service to your address, qualifications, current availability and relevant rental-property experience directly.</p></section></article>'
        schema={'@context':'https://schema.org','@type':'Article','headline':g['title'],'description':g['description'],'datePublished':g['published'],'dateModified':g['modified'],'mainEntityOfPage':origin+route,'author':{'@type':'Organization','name':'Short Term Rental Vendors editorial'},'citation':[g['source']]}
        page(route,g['title'],body,desc=g['description'],schema=schema);dates[route]=g['modified']
    cards=''.join('<article class="card"><h2><a href="/guides/'+g['slug']+'/">'+e(g['title'])+'</a></h2><p>'+e(g['description'])+'</p></article>' for g in guides)
    body=intro('Practical guides for your rental-property team','Prepare clearer scopes, operating records and vendor handoffs before making a decision.','Owner resources')
    body+='<p class="lead">These original guides help owners identify responsibilities, compare proposals and preserve the evidence behind an operating decision. They do not establish that a listed business specializes in short-term rentals.</p><section class="section"><div class="grid owner-guide-grid">'+cards+'</div></section>'
    old=[]
    for f in sorted((Path(root)/'editorial-pages'/'guides').glob('*/index.html')):
        import re,html
        title=html.unescape(re.search(r'<title>(.*?)</title>',f.read_text(),re.S)[1]).split(' | ')[0]
        old.append('<li><a href="/guides/'+f.parent.name+'/">'+e(title)+'</a></li>')
    body+='<section class="section"><h2>Detailed furnishing and purchasing guides</h2><ul class="list">'+''.join(old)+'</ul></section>'
    page('/guides/','Owner guides for rental vendor decisions',body,desc='Original guides for rental-property vendor scopes, records, supplies, maintenance and operating handoffs.');dates['/guides/']='2026-11-20'
    home=Path(root)/'dist'/'index.html'
    text=home.read_text()
    block='<section class="section"><h2>Prepare before choosing a vendor</h2><p>Use practical owner guides to define turnover work, compare service responsibilities and keep clear operating records.</p><p><a class="button" href="/guides/">Explore owner guides</a></p></section>'
    home.write_text(text.replace('</main>',block+'</main>'))
    return dates
