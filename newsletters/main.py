"""
Runs through a lookup file and creates a newsletter file for each association.
The main purpose being to prepare newsletter files for production (which is 
usually broken up per association).

Not entirely useful as it requires to cherry pick the files to use in production.
"""

import csv
from os import path, listdir, makedirs, removedirs, rename

from pyPdf import PdfFileWriter, PdfFileReader

from manifest import Manifest

# This will do something someday
class NewsletterAggregator(object):
    NEWSLETTERS_ROOT = 'documents'
    
    @classmethod
    def aggregate(cls, lookup, manifest):
        pass


stmt_writers = {}
stmt_counts = {}
nl = {}

with open('data.csv', 'rb') as lookup:
    manifest_file = open('documents/manifest.csv', 'rb')
    manifest = Manifest(manifest_file)
    
    reader = csv.DictReader(lookup)
    
    with open('statements.pdf', 'rb') as statements_file:
        statements_pdf = PdfFileReader(statements_file)
        
        counts = {}
        for i, r in enumerate(reader):
            key = r.get('Association Key','').zfill(4)
            name = r.get('Association Name','')
            nlname = r.get('Newsletter Name', '')
            option1 = r.get('Newsletter Option 1', '')
            option2 = r.get('Newsletter Option 2', '')
            account = r.get('Account ID', '')
            
            print 'processing account: {0} {1}'.format(key, account)
            

            docs = manifest.get_for_key(key)
            
            if key not in nl:                
                pdf_writer = PdfFileWriter()
                sheets = 0
                for d in docs:
                    nl_f = open(d.path, 'rb')
                    nl_pdf = PdfFileReader(nl_f)
                    for p in nl_pdf.pages:
                        sheets += 1
                        pdf_writer.addPage(p)
                
                nl[key] = pdf_writer

            if nlname:
                file_root = path.join('tmp', '+{0} on {1} {2}'.format(sheets, option1, option2))
                filename = '{0} {1}.pdf'.format(key, name)
            else:
                file_root = path.join('tmp', '+1 Static')
                filename = 'static'
    
            if not path.exists(file_root):
                makedirs(file_root)
        
            file_path = path.join(file_root, filename)
        
            output = open(file_path, 'wb')
            pdf_writer.write(output)
            
            rename(file_path, file_path.replace('.pdf', ' [{0}].pdf'.format(sheets)))
            
            
            # write out statements
            if nlname:
                filename = '{0} {1} statements.pdf'.format(key, name)
            else:
                filename = 'Static statements.pdf'
    
            stmt_path = path.join(file_root, filename)

            if stmt_path not in stmt_writers:
                stmt_writers[stmt_path] = PdfFileWriter()
            
            stmt_writer = stmt_writers[stmt_path]
            
            stmt_writer.addPage(statements_pdf.getPage(i))
            print 'added stmt {0} to {1}'.format(account, stmt_path)
            
            try:
                stmt_counts[stmt_path] += 1
            except KeyError:
                stmt_counts[stmt_path] = 1
                
        
        for fname, writer in stmt_writers.iteritems():
            with open(fname, 'wb') as output:
                writer.write(output)
            
            rename(fname, fname.replace('.pdf', ' [{0}].pdf'.format(stmt_counts[fname])))
    
    manifest_file.close()