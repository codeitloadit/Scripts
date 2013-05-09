'''
Validates a raw customer data file contains associations we have data for by 
cross referencing a lookup file.

Currently works for APS e.g. Jenark, Voyager VMS.

Can check one file of each type at a time. The following files must be in 
the current directory of where the script is ran from.

Input:
 lookup.csv -- CSV file containing lookup info.
 data.pan -- Raw customer data.
 jenarkdata -- Associations file from a jenark data package.

Output:
 Printed String

Usage:
 > cd /Some/dir
 > ls
 lookup.csv  data.pan
 > python /path/to/validate.py
 Missing Keys: 0001, 0002
'''

import codecs
import csv
import os

# Collect known associations keys from the lookup file
known_keys = []
with codecs.open('lookup.csv', 'rb', 'utf-8-sig') as lookup:
    reader = csv.DictReader(lookup)
    for r in reader:
        known_keys.append(
            r.get('Association Key','').zfill(4)
        )


missing_keys = []

# Collect associations keys from data.pan that are not present in known_keys
if os.path.exists('data.pan'):
    with codecs.open('data.pan', 'rb', 'utf-8-sig') as data:
        reader = csv.reader(data)
        for r in reader:
            key = r[1].zfill(4)
            
            if key not in known_keys:
                if key not in missing_keys:
                    missing_keys.append(key)

# Collect associations keys from jenarkdata that are not present in known_keys
if os.path.exists('jenarkdata'):
    with codecs.open('jenarkdata', 'rb', 'utf-8-sig') as data:
        reader = csv.reader(data)
        for r in reader:
            key = r[0].zfill(4)
            
            if key not in known_keys:
                if key not in missing_keys:
                    missing_keys.append(key)

if not missing_keys:
    print "LOOKS GOOD! :)"
else:
    print 'Missing Keys: ', ', '.join(missing_keys)                
