#!/bin/bash

# Build the MkDocs site
mkdocs build

# Run the convert_html_to_pdf.py script
python convert_html_to_pdf.py
