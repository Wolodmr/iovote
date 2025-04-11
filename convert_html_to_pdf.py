import pdfkit
import os

# Define input and output directories
input_dir = "site"
output_dir = os.path.join(input_dir, "pdfs")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Wkhtmltopdf configuration (make sure the correct path is used)
config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

# PDF conversion options
options = {
    "enable-local-file-access": "",
    "load-error-handling": "ignore",
    "disable-smart-shrinking": "",
    "zoom": "1.3",  # Adjust scaling for better styling
    "dpi": "300",   # Higher DPI for better rendering
    "print-media-type": "",  # Ensures CSS styles are applied correctly
}

# Convert all HTML files in site/ to PDF
for filename in os.listdir(input_dir):
    if filename.endswith(".html"):
        input_html = os.path.join(input_dir, filename)
        output_pdf = os.path.join(output_dir, filename.replace(".html", ".pdf"))
        
        print(f"Converting {input_html} to {output_pdf}...")
        pdfkit.from_file(input_html, output_pdf, configuration=config, options=options)

print("✅ PDF conversion completed!")
