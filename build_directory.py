import json,re,html,pathlib,shutil
P=pathlib.Path(__file__).resolve().parent; D=P/'dist'; shutil.rmtree(D,ignore_errors=True); D.mkdir(parents=True); E=html.escape
slug=lambda s: re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
core={'Florida','Tennessee','Arizona','Oklahoma','Pennsylvania','Texas','Missouri'}
rows='''Alabama|Gulf Shores|Orange Beach
Alaska|Anchorage|Juneau
Arizona|Scottsdale|Mesa|Gilbert|Chandler|Sedona
Arkansas|Hot Springs|Eureka Springs
California|Big Bear Lake|Joshua Tree
Colorado|Denver|Breckenridge
Connecticut|Mystic|New Haven
Delaware|Rehoboth Beach|Bethany Beach
Florida|Panama City Beach|Destin|Fort Walton Beach|Jacksonville|Davenport|Kissimmee|Cape Coral
Georgia|Blue Ridge|Savannah
Hawaii|Honolulu|Kailua-Kona
Idaho|Coeur d'Alene|Boise
Illinois|Chicago|Galena
Indiana|Indianapolis|Bloomington
Iowa|Des Moines|Davenport
Kansas|Wichita|Lawrence
Kentucky|Louisville|Lexington
Louisiana|New Orleans|Baton Rouge
Maine|Portland|Bar Harbor
Maryland|Ocean City|Annapolis
Massachusetts|Boston|Provincetown
Michigan|Traverse City|Grand Rapids
Minnesota|Duluth|Minneapolis
Mississippi|Biloxi|Oxford
Missouri|Branson|Lake Ozark
Montana|Bozeman|Whitefish
Nebraska|Omaha|Lincoln
Nevada|Las Vegas|Reno
New Hampshire|North Conway|Portsmouth
New Jersey|Cape May|Wildwood
New Mexico|Santa Fe|Taos
New York|Lake Placid|Saratoga Springs
North Carolina|Asheville|Wilmington
North Dakota|Fargo|Bismarck
Ohio|Columbus|Logan
Oklahoma|Broken Bow|Hochatown
Oregon|Bend|Portland
Pennsylvania|Lake Harmony|Jim Thorpe|Tobyhanna|Poconos|Hawley
Rhode Island|Newport|Providence
South Carolina|Charleston|Myrtle Beach
South Dakota|Deadwood|Rapid City
Tennessee|Sevierville|Pigeon Forge|Gatlinburg|Nashville|Johnson City
Texas|Austin|Manchaca|Galveston
Utah|Park City|Moab
Vermont|Stowe|Killington
Virginia|Virginia Beach|Luray
Washington|Leavenworth|Seattle
West Virginia|Fayetteville|Berkeley Springs
Wisconsin|Wisconsin Dells|Lake Geneva
Wyoming|Jackson|Cody'''
states={r.split('|')[0]:r.split('|')[1:] for r in rows.splitlines()}
active=set('Panama City Beach|Destin|Fort Walton Beach|Jacksonville|Davenport|Kissimmee|Cape Coral|Scottsdale|Mesa|Gilbert|Chandler|Denver|Branson|Broken Bow|Hochatown|Lake Harmony|Jim Thorpe|Tobyhanna|Poconos|Sevierville|Pigeon Forge|Gatlinburg|Nashville|Johnson City|Austin|Manchaca'.split('|'))
# Category-specific buyer questions, avoiding claims about local laws or availability.
cats={
'Cleaning & turnovers':['Do you support same-day turnovers and holiday arrivals?','What does the checklist cover, and do you send timestamped completion photos?','Who handles linen replacement, supply restocking and damage reporting?'],
'Home inspections':['Can you provide a recent sample report for a comparable property?','Which systems and outbuildings are excluded from the inspection?','Can specialist findings be delivered before the inspection contingency expires?'],
'Property management':['What is the total fee after maintenance markups and booking charges?','Who owns the listing, guest records and photographs if we end the contract?','Can you provide owner references and a sample monthly statement?'],
'Design & furnishing':['Does the written scope include delivery, assembly and packaging removal?','How do you select durable furniture for the intended guest count?','What happens when an item is delayed or arrives damaged?'],
'Photography':['Can you show vacation rental work comparable to this property?','Do the fees include usage rights, twilight shots and revisions?','What are the staging requirements and delivery timeline?'],
'Pool & spa service':['Do you provide written water-test and service logs?','Who responds when equipment fails between guest stays?','Which chemicals, parts and callouts are excluded from the monthly fee?'],
'Real estate agents':['Do you have recent buyer transactions involving the same property type?','Can you separate legal-use diligence from rental revenue estimates?','How will compensation and any referral relationship be disclosed?'],
'Title & closing':['Who verifies title exceptions and recorded restrictions before closing?','Which fees are in the written closing estimate?','How do you independently verify wiring instructions?'],
'Insurance':['Does the proposed policy expressly cover the intended rental activity?','What are the exclusions and deductibles for the specific address?','How are property, liability and interruption coverage coordinated?'],
'Tax & accounting':['Who signs the engagement and is responsible for the tax return?','Which deliverables and years are included in the fee?','How are records, filing deadlines and questions handled?'],
'Cost segregation':['What methodology and supporting documentation does the study provide?','Who reviews the report and supports questions after delivery?','What property records and land-allocation evidence are required?'],
'Handyman services':['Which repairs require a separately licensed trade?','What are your callout fee, hourly rate and after-hours charges?','Can you send photos and obtain approval before additional work?'],
'HVAC':['What does preventive service include for this exact equipment?','Do you offer priority response and disclose diagnostic fees?','Will your quote identify model numbers, permits and warranty terms?'],
'Plumbing':['Can you confirm trade credentials and insurance for the project?','How do you handle emergency leaks when the owner is remote?','Does the estimate include materials, access work and cleanup?'],
'Electrical':['Does the scope include required permits and inspections?','Can you assess the intended occupancy and major equipment loads?','Who documents completed work and warranty coverage?'],
'Roofing':['Will you inspect flashing, drainage and penetrations as well as shingles?','What is the distinction between repair and replacement warranties?','Can you provide itemized materials, disposal and permit costs?'],
'Landscaping':['What work is included in recurring service?','How do seasonal tasks and storm cleanup get priced?','Can you provide completion photos and identify irrigation problems?'],
'Pest control':['Which pests and follow-up visits are covered?','How do treatment instructions affect guest arrival times?','What happens if a guest reports a problem between scheduled visits?'],
'Linen & laundry':['What is the minimum linen inventory for back-to-back stays?','How are lost or damaged items priced?','Do delivery and pickup windows match the turnover schedule?'],
'Smart locks & security':['How are guest codes created, expired and audited?','What is the backup plan if power, internet or a lock fails?','Where will cameras and monitoring devices be installed and disclosed?'],
'Waste & hauling':['What is the collection schedule and overflow policy?','Are bulky items and post-renovation debris priced separately?','Can the property support bear-resistant or other appropriate storage?'],
'Fire & life safety':['Can you assess alarms, extinguishers and exit access for the property?','Who verifies the applicable requirements with the local authority?','Will the final work include inspection and maintenance records?'],
'Permit & zoning support':['Who verifies the exact parcel, jurisdiction and permitted use?','Does the scope include HOA or deed restrictions?','Can you document permit conditions before a purchase commitment?'],
'Lending':['Which loan products fit the intended property and rental use?','What are the reserves, fees and prepayment terms?','Can you confirm the appraisal and closing timeline in writing?']}
V=[]
def add(n,st,city,cat,url,rating=None,count=None,note='',web=None):
 V.append(dict(name=n,state=st,city=city,category=cat,source=url,rating=rating,count=count,note=note,website=web,slug=slug(n)+'-'+slug(city),checked='2026-10-04',evidence='Third-party review source' if rating else 'Published service and customer feedback'))
B='https://reviews.birdeye.com/'
add('Peak Cleaning Service','Arizona','Scottsdale','Cleaning & turnovers',B+'peak-cleaning-service-161480189726085',4.8,260,'Public feedback includes short-term rental owners discussing cleaning and communication.')
add('Beach Bums Cleaning Service, LLC','Florida','Destin','Cleaning & turnovers',B+'beach-bums-cleaning-service-llc-170370347877630',5,11,'Vacation rental owner feedback describes turnover reliability and communication.')
add('K & E Klean 4 U LLC','Texas','Galveston','Cleaning & turnovers',B+'k-e-klean-4-u-llc-166416574298390',5,31,'Owner feedback discusses back-to-back vacation rental cleanings.', 'http://www.keklean4u.com/')
add('Mountain Maids of Breckenridge','Colorado','Breckenridge','Cleaning & turnovers',B+'mountain-maids-of-breckenridge-156205159105869',5,3,'Positive vacation rental feedback is available, but the sample is small and visible reviews are old.')
add('Check-In Ready','Missouri','Branson','Cleaning & turnovers',B+'check-in-ready-156205137053668',5,4,'Owner feedback discusses vacation rental turnovers. The visible sample is small and includes older reviews.')
add('Pocono Pride Cleaning','Pennsylvania','Poconos','Cleaning & turnovers','https://www.homeadvisor.com/rated.PoconoPrideCleaning.80231831.html',5,2,'A January 2025 review describes Airbnb cleaning, scheduling and supply reporting. Small review sample.')
add('Furnishr','National','Multiple markets','Design & furnishing','https://www.trustpilot.com/review/furnishr.com',None,None,'Public customer feedback includes vacation rental furnishing projects. Confirm delivery coverage for your address.','https://furnishr.com/multiple-properties/')
add('ProClean Cabin Cleaning and Inspections','Tennessee','Sevierville','Cleaning & turnovers','https://www.procleancabincleaning.com/client-testimonials',None,None,'Company-published cabin-owner testimonials. An independent rating has not been established here.')
add('Moonshine Cleaners','Tennessee','Sevierville','Cleaning & turnovers','https://moonshinecleaners.com/testimonials/',None,None,'Company-published feedback discusses cabin cleaning. Confirm current service area and availability.','https://moonshinecleaners.com/contact/')
add('ProTrust Cleaning','Pennsylvania','Tobyhanna','Cleaning & turnovers','https://www.yellowpages.com/tobyhanna-pa/mip/protrust-cleaning-550317700',None,None,'Public feedback describes vacation rental cleaning. No numeric rating is reproduced.','https://protrustcleaning.com/house-cleaning/')
add('STR Super Cleaners','Pennsylvania','Poconos','Cleaning & turnovers','https://www.breezeway.io/vacation-rental-cleaning-services/us/poconos',None,None,'A vacation rental industry directory identifies its Poconos cleaning service. Review verification remains pending.','https://strsupercleaners.com/who-we-work-with/')
add('Desert Haven Home Management','Arizona','Sedona','Property management','https://www.bestprosintown.com/az/sedona/desert-haven-home-management-llc-/',None,None,'Public feedback discusses rental cleaning and home care. Sedona is broader directory coverage, not a stated BNB buying market.','https://www.sedonadeserthaven.com/')
add('Aegean Services','Florida','Destin','Cleaning & turnovers','https://www.homeadvisor.com/rated.AegeanCleaningService.103809908.html',None,None,'Public vacation rental owner feedback is available; confirm the latest rating directly.')
add('Branson Premier','Missouri','Branson','Property management','https://www.bbb.org/us/mo/branson/profile/vacation-rentals/branson-premier-0734-1000049742',None,None,'The business profile describes vacation rentals and management. Review guest and owner feedback separately.')
for n,st,city,ident,r,c in [
('Vacation Home Cleaning Services','Florida','Kissimmee','vacation-home-cleaning-services-175451684393015',4.9,42),
('VST Cleaning Services','Florida','Kissimmee','vst-cleaning-services-156204445280840',5,17),
('Premium Cleaning Solutions','Florida','Kissimmee','premium-cleaning-solutions-166443327213708',4.9,37),
('eMaids of Orlando and Kissimmee','Florida','Kissimmee','emaids-of-orlando-and-kissimmee-166400335179413',4.6,22),
('NextLevel Cleaning near Orlando and Kissimmee','Florida','Kissimmee','nextlevel-cleaning-near-orlando-and-kissimmee-166443353528972',4.9,18),
('Merry Maids Kissimmee','Florida','Kissimmee','merry-maids-156204392448019',4.7,281),
('Molly Maid of Kissimmee, St. Cloud and Lakeland','Florida','Kissimmee','molly-maid-of-kissimmee-st-cloud-and-lakeland-156204391594637',4.8,1157),
('Denver Cleaning Service Company','Colorado','Denver','denver-cleaning-service-company-156204414366591',4.8,835),
('BlueSpring Cleaning','Colorado','Denver','bluespring-cleaning-166403354328171',4.8,126),
('Central Park Cleaning','Colorado','Denver','central-park-cleaning-166403365830224',4.7,134),
('Broom','Colorado','Denver','broom-156204305695462',4.9,134),
('EverClean Nashville','Tennessee','Nashville','everclean-nashville-166744478919886',5,247),
('Spokhund Cleaning Nashville','Tennessee','Nashville','spokhund-cleaning-nashville-169750128946867',4.9,515),
('Maid Cleaning Nashville','Tennessee','Nashville','maid-cleaning-nashville-156204538520256',4.9,963),
('Maid in Nashville','Tennessee','Nashville','maid-in-nashville-166425780601415',4.9,212),
('Mirandas Cleaning Service','Tennessee','Nashville','mirandas-cleaning-service-156204539639531',4.7,12),
('Lenir Cleaning Services LLC','Florida','Destin','lenir-cleaning-services-llc-170370695716525',5,6)]:
 add(n,st,city,'Cleaning & turnovers',B+ident,r,c,'Public rating supports consideration. Confirm vacation rental turnover scope, service radius and current capacity directly.')
# Correct exact provider URL from the retrieved record.
next(v for v in V if v['name']=='eMaids of Orlando and Kissimmee')['source']=B+'emaids-of-orlando-and-kissimmee-166400335179413'
# Source identifier corrected to observed search URL below.
next(v for v in V if v['name']=='eMaids of Orlando and Kissimmee')['source']=B+'emaids-of-orlando-and-kissimmee-166400335179413'
add('UrbanNashville Vacation Rentals','Tennessee','Nashville','Property management',B+'urbannashville-vacation-rentals-164598367613704',4.9,448,'Public reviews include an owner discussing rental management. Guest reviews do not establish owner returns.')
add('Honest Pool Care','Arizona','Scottsdale','Pool & spa service',B+'honest-pool-care-166441115920601',4.7,116,'Public feedback discusses recurring pool service and equipment repair.','https://honestpoolcare.com/')
add('Swimright Pool Service & Repair','Arizona','Scottsdale','Pool & spa service',B+'swimright-pool-service-repair-166547742247337',4.6,117,'Public review evidence is available. Confirm address coverage and emergency response.')
add('Reliable Pool Care','Arizona','Scottsdale','Pool & spa service',B+'reliable-pool-care-147149760222178',4.6,28,'The profile describes Scottsdale pool service and repairs; its listed base is Phoenix.')
add('National Property Inspections Greater Scranton','Pennsylvania','Poconos','Home inspections','https://birdeye.com/national-property-inspections-greater-scranton-160735389748257',4.9,98,'Confirm travel radius, current credentials and a sample report before booking.')
add('Daley Home Inspections, LLC.','Tennessee','Nashville','Home inspections',B+'daley-home-inspections-llc-156206391927882',4.9,73,'Based in Mount Juliet. Confirm service for the exact Nashville-area address.')
add('My Visual Listings Orlando','Florida','Kissimmee','Photography','https://www.bestprosintown.com/fl/orlando/my-visual-listings-orlando-real-estate-photography-/',None,None,'The public profile describes photography for vacation property managers. Confirm travel to your address.')
add('Luxe Media Pros','Florida','Kissimmee','Photography','https://www.airbnb.com/services/6985555',5,4,'The Airbnb service listing identifies an Orlando photographer and vacation-home work. Small review sample.')
add('Seed Cleaning & Services LLC','Florida','Destin','Cleaning & turnovers','https://www.cleanwithseed.com/reviews',None,None,'Company-published owner feedback covers Emerald Coast rental cleaning.')
add('Sun Life Cleaning Services','Arizona','Scottsdale','Cleaning & turnovers','https://sunlifecleaning.com/services/airbnb-rental-cleaning-scottsdale/',None,None,'The company publishes STR cleaning scope and customer feedback. Any rating on its site is company-reported.')
# Remove provider whose precise identifier is not retained, rather than guessing.
V=[v for v in V if not v['name'].startswith('eMaids') and v['state']!='Colorado']
(P/'vendors.json').write_text(json.dumps(V,indent=2)); (P/'markets.json').write_text(json.dumps(states,indent=2))
ORIGIN='https://shorttermrentalvendors.com'; CTA='https://www.mybnbaccelerator.com/'; market_source='https://www.bnbaccelerator.com/markets/'
css='''@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');:root{--ink:#102b39;--muted:#536a76;--navy:#082c3c;--teal:#006e6c;--line:#dbe5e9;--pale:#eef5f7;--orange:#faab65}*{box-sizing:border-box}body{margin:0;color:var(--ink);background:#fff;font:16px/1.65 'DM Sans',sans-serif}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}h1,h2,h3,.brand{font-family:Manrope,sans-serif;line-height:1.16;letter-spacing:-.035em}h1{font-size:clamp(2.2rem,4.7vw,4rem);max-width:900px;margin:20px 0}h2{font-size:2rem}h3{font-size:1.23rem;margin:12px 0}.wrap{max-width:1260px;margin:auto;padding:0 30px}header{border-bottom:1px solid var(--line);background:#fff}.header{display:flex;align-items:center;justify-content:space-between;min-height:92px;gap:20px}.brand{color:var(--navy);font-size:20px;font-weight:800;display:flex;align-items:center;gap:12px}.mark{background:var(--navy);color:white;padding:9px 11px;font-size:17px;border-radius:7px;letter-spacing:0}.brand small{display:block;font:12px/1.4 'DM Sans';letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}nav{display:flex;align-items:center;gap:25px}nav a{color:var(--ink);font-weight:600;font-size:14px}.button{display:inline-block;background:var(--teal);color:#fff!important;padding:12px 20px;border-radius:6px;font-weight:700;line-height:1.5}.button:hover{background:#005552;text-decoration:none}.intro{padding:46px 0 25px}.eyebrow{font-size:12px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;color:var(--teal)}.lead{font-size:19px;color:var(--muted);max-width:750px}.searchbox{display:grid;grid-template-columns:2fr 1fr 1fr;gap:12px;margin:30px 0 25px;background:var(--pale);padding:18px;border:1px solid var(--line);border-radius:9px}label{font-size:13px;font-weight:700;display:block}input,select{width:100%;font:16px 'DM Sans';padding:14px;margin-top:7px;border:1px solid #bacbd3;border-radius:5px;background:#fff;color:var(--ink)}input:focus,select:focus{outline:3px solid #90cacb}.featured{display:grid;grid-template-columns:1.25fr 1fr;background:var(--navy);color:white;border-radius:9px;overflow:hidden;margin:24px 0 40px}.featured>div{padding:30px}.featured h2{font-size:28px;margin:10px 0}.featured p{color:#c8dce3;margin:10px 0}.featured .eyebrow{color:var(--orange)}.featured .button{background:var(--orange);color:var(--navy)!important}.feature-side{border-left:1px solid #325362;display:flex;flex-direction:column;justify-content:center}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.card{border:1px solid var(--line);border-radius:8px;padding:23px;background:#fff;display:flex;flex-direction:column;gap:10px}.card p{font-size:15px;margin:0;color:var(--muted)}.card h3 a{color:var(--ink)}.tag{font-size:12px;background:#e5f3f2;color:#00625e;border-radius:4px;padding:4px 8px;display:inline-block;width:fit-content;font-weight:700}.tag.alt{background:#eef1f4;color:#536674}.rating{font-weight:800;font-size:18px;color:#143d4c}.meta{font-size:13px;color:var(--muted)}.card-bottom{margin-top:auto;padding-top:12px;display:flex;justify-content:space-between;gap:10px;font-size:14px;font-weight:700}.section{padding:30px 0}.section-title{display:flex;align-items:center;justify-content:space-between;gap:15px;margin-bottom:22px}.section-title h2{margin:0}.chips{display:flex;flex-wrap:wrap;gap:9px}.chip{border:1px solid var(--line);padding:8px 13px;border-radius:5px;font-size:14px;color:var(--ink)}.chip:hover{background:var(--pale);text-decoration:none}.columns{display:grid;grid-template-columns:2fr 1fr;gap:32px;margin:25px 0 45px}.panel{background:var(--pale);padding:26px;border-radius:8px}.panel h3{margin-top:0}.list{padding-left:22px}.list li{padding:7px 0}.crumbs{font-size:13px;color:var(--muted);padding-top:24px}.empty{padding:30px;border:1px dashed #a5bbc6;background:#f6fafb;border-radius:7px;color:var(--muted)}.result-count{font-size:14px;color:var(--muted)}footer{margin-top:60px;background:var(--navy);color:#c8dce3;padding:40px 0;font-size:14px}footer a{color:#fff}.foot-top{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}.foot-small{max-width:970px;font-size:12px;color:#adc7d0;margin-top:25px}.profile-stat{display:flex;gap:30px;flex-wrap:wrap;padding:25px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.profile-stat strong{display:block;font-size:23px}.profile-stat span{font-size:13px;color:var(--muted)}.directory-link{font-weight:700}.hidden{display:none!important}details{border-bottom:1px solid var(--line);padding:16px 0}summary{font-weight:700;cursor:pointer}.state-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.state-card{padding:20px;border:1px solid var(--line);border-radius:7px}.state-card h3{margin:0 0 8px}@media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}.state-grid{grid-template-columns:repeat(3,1fr)}nav{gap:15px}.columns{grid-template-columns:1fr}}@media(max-width:640px){.wrap{padding:0 18px}.header{align-items:flex-start;flex-direction:column;padding:18px 0;gap:15px}nav{width:100%;flex-wrap:wrap;gap:15px}nav .button{padding:8px 12px}.brand{font-size:18px}.intro{padding-top:30px}.searchbox{grid-template-columns:1fr;padding:14px}.grid,.state-grid,.featured{grid-template-columns:1fr}.featured>div{padding:25px}.feature-side{border-left:0;border-top:1px solid #325362}h1{font-size:2.35rem}.section-title{align-items:flex-start;flex-direction:column}.lead{font-size:17px}.columns{gap:18px}}'''
(D/'style.css').write_text(css)
header='<header><div class="wrap header"><a class="brand" href="/"><span class="mark">SV</span><span>Short Term Rental Vendors<small>Find your property team</small></span></a><nav aria-label="Main navigation"><a href="/markets/">Markets</a><a href="/services/">Services</a><a href="/vendors/">Vendors</a><a class="button" href="'+CTA+'">Buy with BNB Accelerator</a></nav></div></header>'
footer='<footer><div class="wrap"><div class="foot-top"><strong>Short Term Rental Vendors</strong><div><a href="/methodology/">How we select vendors</a> · <a href="/about/">About this directory</a> · <a href="/lending/">Financing introductions</a></div></div><p class="foot-small">BNB Accelerator is this directory’s featured acquisition service. Other listings are research candidates, not a representation that BNB has hired or approved the vendor. Public ratings are dated snapshots and can change. Confirm service scope, credentials, insurance and availability directly. Broader directory coverage does not establish BNB acquisition coverage. This site does not collect visitor submissions or payments.</p></div></footer>'
def featured(place=None):
 text='Sourcing, underwriting, negotiation and launch support for your next short-term rental.' if not place else 'Discuss your buying criteria and confirm whether '+E(place)+' fits BNB Accelerator’s current acquisition coverage.'
 return '<aside class="featured"><div><span class="eyebrow">Featured acquisition service</span><h2>Buy with BNB Accelerator.</h2><p>'+text+'</p></div><div class="feature-side"><p>Start with the property and the operating plan. Build the vendor team around both.</p><a class="button" href="'+CTA+'">Discuss your acquisition</a></div></aside>'
index=[]; allpaths=[]
def page(path,title,body,desc='',indexed=True,schema=None):
 target=D/path.strip('/')/'index.html' if path!='/' else D/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
 url=ORIGIN+path;desc=desc or title+' | Regional vendor information, public review sources and questions to ask before hiring.'
 ld=schema or {'@context':'https://schema.org','@type':'CollectionPage','name':title,'url':url}
 target.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | Short Term Rental Vendors</title><meta name="description" content="'+E(desc,quote=True)+'"><meta name="robots" content="'+('index,follow' if indexed else 'noindex,follow')+'"><link rel="canonical" href="'+url+'"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="/style.css"><meta name="theme-color" content="#082c3c"><script type="application/ld+json">'+json.dumps(ld).replace('<','\\u003c')+'</script></head><body>'+header+'<main class="wrap">'+body+'</main>'+footer+'<script src="/app.js" defer></script></body></html>')
 allpaths.append(path)
 if indexed:index.append(path)
def crumb(text):return '<div class="crumbs"><a href="/">Directory</a> / '+text+'</div>'
def intro(title,sub,eye='Regional vendor directory'):return '<section class="intro"><span class="eyebrow">'+E(eye)+'</span><h1>'+E(title)+'</h1><p class="lead">'+E(sub)+'</p></section>'
def vcard(v):
 rate=str(v['rating'])+' / 5' if v['rating'] else 'Source available'; meta=str(v['count'])+' public reviews' if v['count'] else v['evidence']
 tag='Public rating checked' if v['rating'] and v['count']>=10 else ('Small review sample' if v['rating'] else 'Research candidate')
 return '<article class="card vendor-card" data-search="'+E((v['name']+' '+v['city']+' '+v['state']+' '+v['category']).lower(),quote=True)+'" data-state="'+E(v['state'])+'" data-category="'+E(v['category'])+'"><span class="tag '+('alt' if tag!='Public rating checked' else '')+'">'+tag+'</span><h3><a href="/vendors/'+v['slug']+'/">'+E(v['name'])+'</a></h3><p>'+E(v['city']+' · '+v['state'])+'</p><span class="meta">'+E(v['category'])+'</span><div class="rating">'+rate+'</div><span class="meta">'+E(meta)+' · Checked Oct 4, 2026</span><p>'+E(v['note'])+'</p><div class="card-bottom"><a href="/vendors/'+v['slug']+'/">View profile</a><a href="'+E(v['source'],quote=True)+'" rel="noopener" target="_blank">Review source</a></div></article>'
def vgrid(vs):return '<div class="grid">'+''.join(vcard(v) for v in vs)+'</div>' if vs else '<div class="empty">No source-backed vendor profiles have been published for this selection yet. Use the hiring checklist below while you build your shortlist.</div>'
def filters():return '<div class="searchbox"><label>Find a vendor<input id="query" type="search" placeholder="Business name, market or service"></label><label>State<select id="state"><option value="">All states</option>'+''.join('<option>'+E(s)+'</option>' for s in sorted(set(v['state'] for v in V)))+'</select></label><label>Service<select id="category"><option value="">All services</option>'+''.join('<option>'+E(c)+'</option>' for c in cats)+'</select></label></div><p id="result-count" class="result-count" aria-live="polite"></p><div id="no-results" class="empty hidden">No profiles match these filters. Try a nearby market or another service.</div>'
def checklist(cat):return '<section><h2>Before you hire</h2><ol class="list">'+''.join('<li>'+E(q)+'</li>' for q in cats[cat])+'</ol><p>Ask for a written scope, itemized pricing, recent relevant references and confirmation that the vendor serves your exact address.</p></section>'
def market_path(s,c):return '/markets/'+slug(s)+'/'+slug(c)+'/'
def matched(s,c,cat=None):
 # Only match declared city or regional Poconos coverage, never silently expand service areas.
 return [v for v in V if (v['state']=='National' or (v['state']==s and (v['city']==c or (v['city']=='Poconos' and c in ['Poconos','Tobyhanna','Lake Harmony','Jim Thorpe','Hawley'])))) and (cat is None or v['category']==cat)]
body=intro('Find the team behind your next rental.','Browse vendors by market, service or business name. Start in BNB Accelerator’s core regions, then explore the wider directory.')+filters()+featured()+ '<section class="section"><div class="section-title"><h2>Vendor profiles</h2><a class="directory-link" href="/methodology/">Understand the review evidence</a></div>'+vgrid(V)+'</section><section class="section"><h2>BNB Accelerator’s core states</h2><div class="chips">'+''.join('<a class="chip" href="/states/'+slug(s)+'/">'+s+'</a>' for s in sorted(core))+'</div></section>'
page('/','Short-term rental vendor directory',body,'Find short-term rental cleaners, inspectors, managers, furnishing providers and more. Featured acquisition service: BNB Accelerator.')
page('/vendors/','Browse short-term rental vendors',intro('Find a vendor by name.','Each profile links to its public evidence. Ratings, small samples and company-published feedback are labeled separately.')+filters()+vgrid(V)+featured())
for v in V:
 cat=v['category']; st=v['state']; rate=(str(v['rating'])+' / 5') if v['rating'] else 'Not reproduced'; sample=str(v['count']) if v['count'] else 'See source'
 schema={'@context':'https://schema.org','@type':'ProfilePage','name':v['name']+' vendor profile','url':ORIGIN+'/vendors/'+v['slug']+'/','mainEntity':{'@type':'Organization','name':v['name'],'url':v['website'] or v['source']}}
 body=crumb('<a href="/vendors/">Vendors</a> / '+E(v['name']))+intro(v['name'],v['city']+', '+st+' · '+cat,'Vendor profile')+'<div class="profile-stat"><div><strong>'+rate+'</strong><span>Public rating snapshot</span></div><div><strong>'+sample+'</strong><span>Review sample</span></div><div><strong>Oct 4, 2026</strong><span>Evidence checked</span></div></div><div class="columns"><section><h2>Service and review evidence</h2><p>'+E(v['note'])+'</p><p>This profile helps rental buyers evaluate '+E(v['name'])+' for '+E(cat.lower())+'. A public listing or favorable rating does not confirm current capacity, licensing, insurance or suitability for a specific property.</p><p><a class="button" href="'+v['source']+'" target="_blank" rel="noopener">Open public source</a></p><p>'+('<a href="'+v['website']+'">Visit provider website</a>' if v['website'] else 'Contact options are available on the linked public profile.')+'</p>'+checklist(cat)+'</section><aside class="panel"><h3>Read the evidence carefully</h3><p>'+('This profile has fewer than 10 reviews. Use recent property-owner references to supplement the small sample.' if v['rating'] and v['count']<10 else 'Read recent negative and positive feedback, the vendor’s response and whether the reviewer was an owner or a guest.')+'</p><p>'+('No independent numeric rating is reproduced. The source supports research, not a verified recommendation.' if not v['rating'] else 'The rating is reproduced from the linked public source, not collected by this directory. Open the source for its latest value.')+'</p><a href="/methodology/">Our selection method</a></aside></div>'+featured(v['city'])
 page('/vendors/'+v['slug']+'/',v['name']+' services and review sources',body,schema=schema)
services='<div class="grid">'+''.join('<a class="card" href="/services/'+slug(c)+'/"><h3>'+E(c)+'</h3><p>'+str(sum(v['category']==c for v in V))+' published profiles</p></a>' for c in cats)+'</div>'
page('/services/','Short-term rental vendor services',intro('Build the team around the property.','From due diligence to guest-ready operations, use a separate written scope for each service.')+services+featured())
for cat in cats:
 vs=[v for v in V if v['category']==cat]; lending=cat=='Lending'
 body=intro(cat+' for short-term rentals','Compare the evidence, ask focused questions and confirm the service for your property.')
 body+=('<div class="panel"><h2>Financing introductions through BNB Accelerator</h2><p>Discuss the property, intended rental use and borrowing needs with BNB Accelerator. No individual lender is promoted here until the directory receives a confirmed approved partner list.</p><a class="button" href="'+CTA+'">Request a financing introduction</a></div>' if lending else vgrid(vs))+checklist(cat)+featured()
 page('/services/'+slug(cat)+'/',cat+' vendor directory',body,indexed=bool(vs) or lending)
markets_body=intro('Start with the market.','The core footprint comes from BNB Accelerator’s published market page. Other locations are wider directory coverage and do not imply acquisition availability.')+'<div class="state-grid">'
for s,cs in states.items():
 if s=='Colorado':
  page('/states/colorado/','Colorado coverage',intro('Explore other regions first.','Colorado is not a priority for this directory. Start with Florida, Tennessee, Arizona, Oklahoma, Pennsylvania, Texas or Missouri.')+featured(),indexed=False)
  continue
 vs=[v for v in V if v['state']==s]
 markets_body+='<a class="state-card" href="/states/'+slug(s)+'/"><span class="tag '+('' if s in core else 'alt')+'">'+('Core state' if s in core else 'Wider directory')+'</span><h3>'+s+'</h3><span class="meta">'+str(len(cs))+' markets · '+str(len(vs))+' profiles</span></a>'
 body=crumb(s)+intro(s+' short-term rental vendors','Browse '+s+' market checklists and published vendor profiles. '+('BNB Accelerator identifies this as one of its core acquisition states.' if s in core else 'This state is broader directory coverage. BNB Accelerator acquisition service is not confirmed here.'))+'<p><a href="'+market_source+'">Source: BNB Accelerator’s published markets</a></p><div class="chips">'+''.join('<a class="chip" href="'+market_path(s,c)+'">'+E(c)+'</a>' for c in cs)+'</div><section class="section"><h2>Published providers in '+s+'</h2>'+vgrid(vs)+'</section>'+featured(s)
 page('/states/'+slug(s)+'/',s+' short-term rental vendor directory',body,indexed=s in core or bool(vs))
 for c in cs:
  vs=matched(s,c);isactive=c in active and s in core
  body=crumb('<a href="/states/'+slug(s)+'/">'+s+'</a> / '+E(c))+intro(c+' short-term rental vendors','Find service profiles and hiring checklists for '+c+', '+s+'. '+('This location is within BNB Accelerator’s published core market coverage; confirm the specific address and purchase criteria.' if isactive else 'This is broader directory coverage, not confirmation that BNB Accelerator buys in this location.'))
  body+='<p><a href="'+market_source+'">Check BNB Accelerator’s current market coverage</a></p>'+vgrid(vs)+'<section class="section"><h2>Service checklists for '+E(c)+'</h2><div class="chips">'+''.join('<a class="chip" href="'+market_path(s,c)+slug(cat)+'/">'+E(cat)+'</a>' for cat in cats)+'</div></section>'+featured(c)
  page(market_path(s,c),c+', '+s+' short-term rental vendors',body,indexed=bool([v for v in vs if v['state']!='National']))
  for cat in cats:
   cvs=matched(s,c,cat); haslocal=bool([v for v in cvs if v['state']!='National']);lending=cat=='Lending'
   body=crumb('<a href="/states/'+slug(s)+'/">'+s+'</a> / <a href="'+market_path(s,c)+'">'+E(c)+'</a> / '+E(cat))+intro(cat+' in '+c, 'Use this checklist when evaluating '+cat.lower()+' for a short-term rental in '+c+', '+s+'. Confirm exact-address coverage before hiring.','Market hiring checklist')
   body+=('<div class="panel"><h2>Request a financing introduction</h2><p>BNB Accelerator can discuss your intended purchase and route an inquiry to its approved financing network. This page does not promote an individual lender.</p><a class="button" href="'+CTA+'">Contact BNB Accelerator</a></div>' if lending else vgrid(cvs))+checklist(cat)+'<p><a href="/services/'+slug(cat)+'/">Browse all '+E(cat.lower())+' profiles</a></p>'+featured(c)
   page(market_path(s,c)+slug(cat)+'/',cat+' in '+c+', '+s,body,indexed=haslocal)
page('/markets/','Browse rental vendor markets',markets_body+'</div>'+featured())
page('/lending/','Short-term rental financing introductions',intro('Financing starts with the property.','Discuss your purchase with BNB Accelerator and request an introduction from its approved network.')+'<a class="button" href="'+CTA+'">Request an introduction</a>'+checklist('Lending')+'<p>No lender names, rates or approval claims are published without confirmed partner authorization.</p>')
page('/methodology/','How we select and describe vendors',intro('A source you can open. A claim you can check.','Every published profile links to the evidence used to describe it.')+'<div class="columns"><section><h2>Our review standard</h2><p>Profiles with a public rating of at least 4.5 out of 5 and at least 10 reviews receive the “Public rating checked” label. This label describes the evidence, not an inspection of the business or a guarantee of service.</p><p>Positive profiles with fewer than 10 reviews carry a small-sample label. Company testimonials and service directories are research candidates, with no independent numeric rating inferred.</p><h2>What a listing does not establish</h2><p>A favorable rating does not establish current licensing, insurance, availability, price or property-specific service. Some profiles cover general residential services. Confirm vacation rental experience separately.</p><h2>Coverage and dates</h2><p>Review snapshots were researched October 4, 2026. Search providers may serve cached content, so the source can be older than our research date. Follow the source for the latest reviews.</p><h2>Acquisition and lending</h2><p>BNB Accelerator is the featured acquisition service. Competing acquisition companies are excluded from this directory’s acquisition promotion. Agents may be considered as transaction professionals, subject to credential and scope checks. Lending inquiries go to BNB until named lending partners are authorized.</p></section><aside class="panel"><h3>Before signing</h3><ol class="list"><li>Confirm identity and exact service area.</li><li>Verify credentials and insurance.</li><li>Read recent critical feedback and responses.</li><li>Speak to recent relevant owner references.</li><li>Agree to a written scope and cancellation terms.</li></ol></aside></div>')
page('/about/','About Short Term Rental Vendors',intro('A directory for buyers and owners.','Find the professionals who help evaluate, close, launch and operate a short-term rental.')+'<p>BNB Accelerator is this directory’s featured acquisition service. Its purchase inquiries are routed to <a href="'+CTA+'">mybnbaccelerator.com</a>. This is a promotional relationship and should be considered when using the directory.</p><p>Other vendors are listed from public sources. A listing does not imply an existing BNB partnership or endorsement. The directory distinguishes BNB’s core acquisition footprint from broader national vendor research.</p><p>To discuss an acquisition or send a directory correction, contact BNB Accelerator through its website.</p>'+featured())
(D/'app.js').write_text('''(()=>{const q=document.getElementById('query'),s=document.getElementById('state'),c=document.getElementById('category');if(!q)return;const cards=[...document.querySelectorAll('.vendor-card')];function filter(){let n=0;for(const card of cards){const show=card.dataset.search.includes(q.value.toLowerCase().trim())&&(!s.value||card.dataset.state===s.value)&&(!c.value||card.dataset.category===c.value);card.classList.toggle('hidden',!show);if(show)n++}document.getElementById('result-count').textContent=n+' vendor profile'+(n===1?'':'s');document.getElementById('no-results').classList.toggle('hidden',n!==0)}for(const x of [q,s,c])x.addEventListener('input',filter);filter()})();''')
(D/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
(D/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+ORIGIN+p+'</loc><lastmod>2026-10-04</lastmod></url>' for p in index)+'</urlset>')
(D/'404.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="/style.css"></head><body>'+header+'<main class="wrap">'+intro('Page not found.','Return to the directory to find a vendor, market or service.')+'<a class="button" href="/">Open directory</a></main>'+footer+'</body></html>')
(P/'build-summary.json').write_text(json.dumps({'pages':len(allpaths),'indexable_pages':len(index),'noindex_checklists':len(allpaths)-len(index),'vendors':len(V),'states':len(states),'markets':sum(len(cs) for st,cs in states.items() if st!='Colorado'),'categories':len(cats),'lending_partners_published':0},indent=2))
(P/'README.md').write_text('''# Short Term Rental Vendors\n\nStatic source-backed directory. Run `python build_directory.py` from this checkout to regenerate. Public source data lives in vendors.json and markets.json; the initial generator is build_directory.py. No credentials or private client data are included. BNB Accelerator is the only promoted acquisition service. Financing routes to BNB until a named partner list is confirmed. Never infer a lending partner from a vendor submission.\n\nPages with no local vendor evidence are noindex and excluded from the sitemap. Promote them to index only after verified local vendor information and original service-area detail are added. Review dates describe research time, not source freshness. No third-party aggregate review rich-result schema is emitted.\n''')

print((P/'build-summary.json').read_text())

# IndexNow ownership key survives regeneration.
INDEXNOW_KEY='11ab8efccb1419e8ed2eb8c7b552c457'
(D/(INDEXNOW_KEY+'.txt')).write_text(INDEXNOW_KEY,encoding='utf-8')

INDEXNOW_KEY='da5c6d1135a38b6e38c92beb44d2eb05'
(D/(INDEXNOW_KEY+".txt")).write_text(INDEXNOW_KEY,encoding="utf-8")
