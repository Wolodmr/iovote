from weasyprint import HTML
import os

input_path = os.path.abspath("site/deployment/index.html")
output_path = os.path.abspath("docs/pdfs/deployment.pdf")
base_url = os.path.dirname(input_path)

HTML(input_path, base_url=base_url).write_pdf(output_path)
