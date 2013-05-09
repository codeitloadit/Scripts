import warnings
warnings.filterwarnings(action="ignore")
from pyPdf import PdfFileWriter, PdfFileReader
import os
import subprocess

#PATH = r"/Volumes/Data/_brian/PDF2JPG"
PATH = r"/Users/brian/Downloads"
subprocess.call('mkdir /Users/brian/Downloads/OUTPUT', shell=True)

for root, dirs, files in os.walk(PATH):
    for f in files:
        if (str(f).upper().endswith('.PDF')):
            ROOT_DASH = root + '/'
            pdf_name = str(f)
            pdf_nameOnly = str(f).upper().replace('.PDF','')
                     
            print '\n----------\n'
            print pdf_name
            print '\n----------\n'
              
        # Add BLANK to begining of PDF.
            inputStream = file(ROOT_DASH + pdf_name, 'rb')
            input = PdfFileReader(inputStream)

            tempFile = ROOT_DASH + 'OUTPUT/' + pdf_name
            temp = PdfFileWriter()
            blank = PdfFileReader(file('/Users/brian/Documents/BLANK.pdf', 'rb'))

            temp.addPage(blank.getPage(0))

            # Copy the input pdf to the output.
            for page in range(int(input.getNumPages())):
                temp.addPage(input.getPage(page))


            # Write the temp to pdf.
            tempStream = file(tempFile, 'wb')
            temp.write(tempStream)
            tempStream.close()
            inputStream.close()


print '\n\nFinished!\n\n'