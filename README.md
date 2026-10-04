# Short Term Rental Vendors

Static source-backed directory. Run `python build_directory.py` from this checkout to regenerate. Public source data lives in vendors.json and markets.json; the initial generator is build_directory.py. No credentials or private client data are included. BNB Accelerator is the only promoted acquisition service. Financing routes to BNB until a named partner list is confirmed. Never infer a lending partner from a vendor submission.

Pages with no local vendor evidence are noindex and excluded from the sitemap. Promote them to index only after verified local vendor information and original service-area detail are added. Review dates describe research time, not source freshness. No third-party aggregate review rich-result schema is emitted.

## Vercel deployment

Import this repository in Vercel. Framework preset: Other. The included vercel.json builds with Python and serves dist. Connect shorttermrentalvendors.com and redirect www to the apex. Keep canonical URLs on the apex.

## Search submission

After the custom domain and HTTPS work, run python3 submit_indexnow.py. It checks the live ownership key before submitting the 92 sitemap URLs. Submit https://shorttermrentalvendors.com/sitemap.xml in the verified Google Search Console property. Submission does not guarantee indexing.

## Verified vendor expansion

`verified-vendors.json` contains official public business location contacts. The generator merges these with the original curated profiles; `vendor-source-audit.json` records source directories and excluded records. Listings describe local service locations, which may share a franchise owner, rather than claiming each is an unrelated company. Email addresses are published only when explicitly verified.

Run `python3 build_directory.py`, `python3 verify.py`, and `python3 verify_expansion.py`. Every vendor profile has a canonical URL, index/follow metadata, structured contact data where available, sitemap inclusion, a crawlable directory link, and BNB Accelerator promotion. Empty market checklists retain noindex. Profiles do not claim a provider has confirmed vacation-rental experience or a BNB partnership.

The directory uses 48 profiles per static page. All profiles can be found through ordinary pagination with JavaScript disabled. Search loads a public summary file on demand and searches the full directory.
