# Short Term Rental Vendors

Static source-backed directory. Run `python build_directory.py` from this checkout to regenerate. Public source data lives in vendors.json and markets.json; the initial generator is build_directory.py. No credentials or private client data are included. BNB Accelerator is the only promoted acquisition service. Financing routes to BNB until a named partner list is confirmed. Never infer a lending partner from a vendor submission.

Pages with no local vendor evidence are noindex and excluded from the sitemap. Promote them to index only after verified local vendor information and original service-area detail are added. Review dates describe research time, not source freshness. No third-party aggregate review rich-result schema is emitted.

## Vercel deployment

Import this repository in Vercel. Framework preset: Other. The included vercel.json builds with Python and serves dist. Connect shorttermrentalvendors.com and redirect www to the apex. Keep canonical URLs on the apex.

## Search submission

After the custom domain and HTTPS work, run python3 submit_indexnow.py. It checks the live ownership key before submitting the 92 sitemap URLs. Submit https://shorttermrentalvendors.com/sitemap.xml in the verified Google Search Console property. Submission does not guarantee indexing.
