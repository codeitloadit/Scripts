import warnings
warnings.filterwarnings(action="ignore")
import csv
import os
import subprocess

subprocess.call('clear', shell=True)
working_dir = r'/Users/Brian/Downloads'
key = 0
lookup_keys = list()
missing_assoc = list()

for root, dirs, files in os.walk(working_dir):
    for f in files:
        if str(f).endswith('_lookup.csv'):
            fin = open(os.path.join(root, f))
            lookup_file = fin.readlines()
            fin.close()
        
    for f in files:
        if not str(f).endswith('_lookup.csv'):
            fin = open(os.path.join(root, f))
            data_file = fin.readlines()
            fin.close()
          
lookup_reader = csv.reader(lookup_file, delimiter = ",", skipinitialspace=True)
data_reader = csv.reader(data_file, delimiter = ",", skipinitialspace=True)

for lookup_assoc in lookup_reader:
    lookup_keys.append(lookup_assoc[key])
    
for data_assoc in data_reader:
    if data_assoc[key].strip() not in lookup_keys and data_assoc[key].strip() not in missing_assoc: 
        missing_assoc.append(data_assoc[key].strip())
            
if len(missing_assoc) > 0:
    print 'Missing {0} association(s):'.format(len(missing_assoc))
    for assoc in missing_assoc:
        print assoc
else:
    print 'All associations in the Data File are present in the Lookup File'

print ''
    
            