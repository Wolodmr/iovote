from weasyprint import HTML

HTML('site/deployment/index.html', base_url='site/deployment/').write_pdf('docs/pdfs/deployment.pdf')
