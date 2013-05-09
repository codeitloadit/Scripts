import copy
import csv
from os import path

class Manifest(object):
    def __init__(self, file):
        self.file = file
        
        self.data = {}
        
        self.parse()
        
    def parse(self):
        reader = csv.DictReader(self.file)
        for r in reader:
            key = r.get('association_key','').zfill(4)
            if key not in self.data:
                self.data[key] = []
            self.data[key].append(Document(r))
    
    def get_for_key(self, key):
        documents = copy.deepcopy(self.data.get(key))
        if not documents:
            documents = []
        statics = self.data.get('STATIC',None)
        if statics:
            for d in statics:
                documents.append(d)
        return documents

class Document(object):
    def __init__(self, document_dict):
        self.data = document_dict
    
    def __repr__(self):
        return u'{0}'.format(self.path)
    
    @property
    def path(self):
        return path.join('documents', self.data.get('formatted_name'))
    
    @property
    def association(self):
        return self.data.get('association_key')