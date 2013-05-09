"""
Runs through a lookup file and creates a newsletter file for each association.
The main purpose being to prepare newsletter files for production (which is 
usually broken up per association).

Not entirely useful as it requires to cherry pick the files to use in production.
"""

import csv
from os import path, listdir, makedirs, removedirs, rename, remove

from pyPdf import PdfFileWriter, PdfFileReader

from manifest import Manifest
from statements import StatementSet

DEST_DIR = 'proofs'

with open('data.csv', 'rb') as of:
    with open('statements.pdf') as stmtspdf:
        statements = StatementSet.parse_from_file(stmtspdf, of)
        
        manifest_file = open('documents/manifest.csv', 'rb')
        manifest = Manifest(manifest_file)
        
        for s in statements:
            key = s.association
            stmtpdfs = statements.create_pdf(
                destination=DEST_DIR, group=True, association_key=key)
            
            docs = manifest.get_for_key(key)
            nl_count = len(docs)
            
            for i, f in enumerate(stmtpdfs):
                fpath = f.name
                f.close()
                f = open(fpath, 'rb')
                stmtreader = PdfFileReader(f)
                
                assocwriter = PdfFileWriter()
                for pi, p in enumerate(stmtreader.pages):
                    assocwriter.addPage(p)
                    
                    for d in docs:
                        nl_f = open(d.path, 'rb')
                        nl_pdf = PdfFileReader(nl_f)
                        for nl_p in nl_pdf.pages:
                            assocwriter.addPage(nl_p)
                
                with open(path.join(DEST_DIR, '{0} - {1} [stmt + {2}].pdf'.format(key, s.association_name, nl_count)), 'wb') as output:
                    assocwriter.write(output)
                f.close()
                remove(fpath)
            
            
            # smush all files at end
            proofwriter = PdfFileWriter()
            for f in listdir(DEST_DIR):
                pass
                
        
        manifest_file.close()
