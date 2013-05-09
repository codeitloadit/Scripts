import warnings
warnings.filterwarnings(action="ignore")
import csv
import os

path = raw_input('Optimal File: ')
root, filename = os.path.split(path)

reader = csv.reader(open(path), delimiter = ',', skipinitialspace=True)
headers = reader.next()

output = list()

output.append('[' + filename + ']')
output.append('CharacterSet=UTF-8')

for i, header in enumerate(headers):
    output.append('Col{0}="{1}" Text'.format(i+1, header))
    
fout = file(os.path.join(root, 'Schema.ini'), 'w')
for line in output:
    fout.write('{0}{1}'.format(line, '\n'))
fout.close()