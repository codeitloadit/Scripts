import csv
from os import path, listdir, makedirs, removedirs

from pyPdf import PdfFileWriter, PdfFileReader

# Isn't really being used right now...
class Statement(object):
    """
    Represents a single statement sheet.
    """
    
    def __init__(self, file, data):
        """
        Takes a statement file object and a dictionary of 
        data used to make up the statement.
        """
        
        self.file = file
        self.data = data
    
    @property
    def association(self):
        """Returns associatoin key for statement."""
        
        return self.data.get('Association Key','')
    
    @property
    def association_key(self):
        return self.association
    
    @property
    def association_name(self):
        return self.data.get('Association Name','')
    
    @property
    def account(self):
        """Returns account id for statement."""
        
        return self.data.get('Account ID','')


# This is what you want!!!
class StatementSet(list):
    """
    Represents a set of statements.
    """
    
    ACCOUNT_ID = 'Account ID'
    ASSOCIATION_KEY = 'Association Key'
    
    DEFAULT_SPLIT_FIELD = ACCOUNT_ID
    
    def __init__(self, pdf):
        self.pdf = pdf
        self.pdf_reader = PdfFileReader(self.pdf)
    
    def create_pdf(self, destination=None, group=False, *args, **kwargs):
        """
        Given a keyword argument that matches a field of Statement, will create a pdf
        for that record.
        """
        
        if not path.exists(destination):
            makedirs(destination)
        result = []
        writer = PdfFileWriter()        
        match_cnt = 1
        for k, v in kwargs.iteritems():
            if k == 'destination' or k == 'group':
                continue
            for i, s in enumerate(self):
                stmt_val = getattr(s, k, '')
                if stmt_val == v:
                    # create a pdf                    
                    if group:
                        filename = '{0}_{1}.pdf'.format(k, v)
                    else:
                        filename = '{0}_{1}_{2}.pdf'.format(k, v, match_cnt)
                        writer = PdfFileWriter()
                        
                    full_path = path.join(destination, filename)
                    
                    writer.addPage(self.get_pdf_page(i))
                    
                    if not group:
                        output = open(full_path, 'wb')
                        writer.write(output)
                        result.append(output)
                        match_cnt += 1
                    
        if group:
            if full_path:
                output = open(full_path, 'wb')
                writer.write(output)
                result.append(output)
        
        return result
                
    
    def get_pdf_page(self, page_num):
        return self.pdf_reader.getPage(page_num)
    
    @classmethod
    def parse_from_file(cls, file, optimalfile):
        """
        Takes a file of statements and optimalfile.
        Assums the optimalfile and file are sorted 
        identically.
        """
        
        inst = StatementSet(file)

        reader = csv.DictReader(optimalfile)
        
        for data in reader:
            pdf = 'test.pdf'
            inst.append(Statement(pdf, data))
        
        return inst
    
    @classmethod
    def split(cls, file, optimalfile, dest_dir='.', fields=None):
        """
        Splits a statements pdf on a given field and saves them
        to the dest_dir.
        
        Assumes `optimalfile` and `file` are sorted identically.
        """
        
        splits = {}
        counts = {}
        
        if not fields:
            fields = [StatementSet.DEFAULT_SPLIT_FIELD]
        
        if not path.exists(dest_dir):
            makedirs(dest_dir)
        
        pdf_reader = PdfFileReader(file)
        for ri, r in enumerate(optimalfile):
            token = ''
            for f in fields:
                token += r.get(f).replace(' ', '_')

            if not token:
                token = 'blank'

            # Cache the file so we can keep adding to it
            # on subsequent loops 
            if token not in splits:
                splits[token] = PdfFileWriter()
            
            if token not in counts:
                counts[token] = 0
            
            counts[token] += 1
            
            split = splits[token]
            
            split.addPage(pdf_reader.getPage(ri))
        
        # remember, split is a pdf writer object
        for token, split in splits.iteritems():
            file_path = path.join(
                dest_dir, '{0} [{1}].pdf'.format(
                token, counts[token])
            )
            
            with open(
                file_path, 'wb') as output:
                split.write(output)
            
                yield file_path
            