import warnings
warnings.filterwarnings(action="ignore")
from pyPdf import PdfFileWriter, PdfFileReader
import os
from os.path import join
import subprocess

NLKEY = 'XX.jpg'
PATH = r'/Users/brian/Downloads'
TMPOUT = str(join(PATH, 'tmpout.txt'))
OUT = ''

for root, dirs, files in os.walk(PATH):
    for f in files:
        if str(f).upper().endswith('.PDF') and len(str(f)) != 12: #HACK!
            pdfin = PdfFileReader(file(join(root, f), 'rb'))
            pdfout = PdfFileWriter()
            OUT = str(join(root, str(f).replace('.pdf', '_OUT.pdf')))
            
            for page in range(int(pdfin.getNumPages())):
                print 'Processing page ' + str(page + 1) + ' of ' + str(pdfin.getNumPages())
                pdfout.addPage(pdfin.getPage(page))
                
                subprocess.call('pdf2txt.py -o ' + TMPOUT + ' -p ' + str(page + 1) + ' ' + str(join(root, f)), shell=True)
                
                txtin = open(TMPOUT).read()
                if NLKEY in txtin:
                    nlcode = txtin[txtin.find(NLKEY) - 6 : txtin.find(NLKEY)]
                    
                    nlfound = False
                    for nl in files:
                        if nlcode in str(nl):
                            pdfnl = PdfFileReader(file(join(root, nl), 'rb'))
                            nlfound = True
                    
                    if not nlfound:
                        print 'Missing ' + nlcode
                    
                    for nlpage in range(int(pdfnl.getNumPages())):
                        pdfout.addPage(pdfnl.getPage(nlpage))
                        
            
            fout = file(OUT, 'wb')
            pdfout.write(fout)
            fout.close()
                        
print '\n\nFinished!\n\n'
