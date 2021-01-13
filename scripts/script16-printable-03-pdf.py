
import pdfkit 
options = {
  "enable-local-file-access": None,
  'page-size': 'Letter',
    'margin-top': '1.25in',
    'margin-right': '1in',
    'margin-bottom': '0.75in',
    'margin-left': '1.25in',
    'image-dpi' : '850',
    'footer-font-size': '8',
    'header-font-size': '8',
    'header-right': 'World\'s Women 2020',
    'footer-line': None,
    'footer-right': 'Statistics Division',
    'footer-left': 'United Nations Department of Economic and Social Affairs',
}


pdfkit.from_file('printable/html/0d1ff2530f17451bb8437c6ea584282e.html',  'printable/pdf/0d1ff2530f17451bb8437c6ea584282e.pdf', options=options) 
