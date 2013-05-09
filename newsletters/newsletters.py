"""
Takes an output/data/optimal file, iterates over it, splits statements per record
and places corresponding newsletters behind everyone.
"""

import csv
from os import path, listdir, makedirs, removedirs

from pyPdf import PdfFileWriter, PdfFileReader

from manifest import Manifest

TMP_PATH = 'tmp'

makedirs(TMP_PATH)

statements = PdfFileReader(open('statements.pdf', 'rb'))

manifest_file = open('documents/manifest.csv', 'rb')
manifest = Manifest(manifest_file)

with open('output.csv', 'rb') as output_data:
    data_reader = csv.DictReader(output_data)
    for ri, row in enumerate(data_reader):
        key = row.get('Association Key','').zfill(4)
        account_id = row.get('Account ID','')
        
        output = PdfFileWriter()
        output.addPage(statements.getPage(ri))
        
        newsletters = manifest.get_for_key(key)
        for nl in newsletters:
            nl_f = open(nl.path, 'rb')
            nl_pdf = PdfFileReader(nl_f)
            for p in nl_pdf.pages:
                output.addPage(p)
            nl_f
        
        with open(path.join(TMP_PATH, key + '_' + account_id + '.pdf'), 'wb') as output_stream:
            output.write(output_stream)
            
proof_pdfs = listdir(TMP_PATH)
proof_pdfs = [f for f in proof_pdfs if f != '.DS_Store']

PDF_FLUSH = 50
OUTPUT_FILENAME = 'proofs_{0}.pdf'

# initialize output
flushi = 0
outputfname = OUTPUT_FILENAME.format(flushi)
output = PdfFileWriter()
output_stream = open(outputfname, 'wb')
pdf_cache = []
total = len(proof_pdfs)
for pdfi, f in enumerate(proof_pdfs):
    print pdfi, f
    # begin terrible flushing algo
    # there is a better way to handle this
    # but I was pressed for time.
    # It will generate a file for each flush,
    # and not clean up after itself.
    # The last file is the one you want.
    if (pdfi % PDF_FLUSH) == 0:
        
        print 'Flushing...'
        output.write(output_stream)
        output_stream.close()
        output = PdfFileWriter()
        try:
            outputr.close()
        except NameError, e:
            print e
            print 'First run. No output.'
            
        outputr = open(outputfname, 'rb')
        output_pdf = PdfFileReader(outputr)
        for pi, p in enumerate(output_pdf.pages):
            print '  added page {0}'.format(pi)
            output.addPage(p)

        for cf in pdf_cache:
            cf.close()
    
        flushi += 1
        outputfname = OUTPUT_FILENAME.format(flushi)
        output_stream = open(outputfname, 'wb')
            
    f = open(path.join(TMP_PATH, f), 'rb')
    pdf_cache.append(f)
    f_pdf = PdfFileReader(f)
    for p in f_pdf.pages:
        output.addPage(p)
    
    if (pdfi + 1) == total:
        output.write(output_stream)
        output_stream.close()

#removedirs(TMP_PATH)
manifest_file.close()