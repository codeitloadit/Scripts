import warnings
warnings.filterwarnings(action="ignore")
import csv
import os

path = raw_input('Optimal File: ')
key = raw_input('Association Key: ')

root, filename = os.path.split(path)

reader = csv.reader(open(path), delimiter = ',', skipinitialspace=True)
output = list()

remove_assoc = False
if key.endswith('-rm'):
    remove_assoc = True
    key = key.replace('-rm', '').strip()
    
for i, line in enumerate(reader):
    lineout = ''
    
    if i == 0 and not remove_assoc:
        for field in line:
            lineout += '"{0}",'.format(field)
        output.append(lineout.strip(',') + '\n')
    if remove_assoc:
        if line[2] != key:
            for field in line:
                lineout += '"{0}",'.format(field)
            output.append(lineout.strip(',') + '\n')
    
    else:
        if line[2] == key:
            for field in line:
                lineout += '"{0}",'.format(field)
            output.append(lineout.strip(',') + '\n')
if remove_assoc:
    key = key + '_removed'
    
outpath = os.path.join(root, key + '.csv')

fout = file(outpath, 'w')     
for line in output:
    fout.write(line)
fout.close()