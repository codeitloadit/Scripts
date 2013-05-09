import warnings
warnings.filterwarnings(action="ignore")
from pyPdf import PdfFileWriter, PdfFileReader
import os
import subprocess

# PATH = r"/Volumes/Data/_brian/PDF2JPG"
PATH = r"/Users/Brian/Downloads"

for root, dirs, files in os.walk(PATH):        
    for f in files:
        if str(f).upper().endswith('.PDF'):
            ROOT_DASH = root + '/'
            pdf_name = str(f)
            pdf_nameOnly = pdf_name[0:6]
            
            print '\n----------\n'
            print pdf_name
            print '\n----------\n'                     
        
        # Split PDF to JPG.                       
            subprocess.call('gs -sDEVICE=jpeg -dJPEGQ=100 -dGraphicsAlphaBits=4 \
            -dTextAlphaBits=4 -dDOINTERPOLATE -sOutputFile="' + ROOT_DASH + pdf_nameOnly + '%02d.jpg" \
            -dSAFER -dBATCH -dNOPAUSE -r300x300 "' + ROOT_DASH + pdf_name + '"', shell=True)

        # Split PDF to TIF.
#             subprocess.call('gs -sDEVICE=tiffpack -dJPEGQ=100 -dGraphicsAlphaBits=4 \
#             -dTextAlphaBits=4 -dDOINTERPOLATE -sOutputFile="' + ROOT_DASH + pdf_nameOnly + '%02d.tif" \
#             -dSAFER -dBATCH -dNOPAUSE -r300x300 "' + ROOT_DASH + pdf_name + '"', shell=True)

print '\n\nFinished!\n\n'
