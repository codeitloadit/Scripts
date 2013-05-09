import warnings
warnings.filterwarnings(action="ignore")
import csv
import os

full_file = raw_input('Full File: ')
part_file = raw_input('Partial File: ')

root, filename = os.path.split(full_file)

full_reader = csv.reader(open(full_file), delimiter = ',', skipinitialspace=True)
part_reader = csv.reader(open(part_file), delimiter = ',', skipinitialspace=True)

output = ''

full_list = list(full_reader)
part_list = list(part_reader)

for f_line in full_list:
    is_in_partial = False
    for p_line in part_list:
        if p_line[0] == f_line[0]:
            is_in_partial = True
            break

    if not is_in_partial:
        for field in f_line:
            if ',' in field:
                output += '"' + field + '",'
            else:
                output += field + ','
        output += '\n'

outpath = os.path.join(root, 'Missing Records - {0}.csv'.format(len(output.split('\n'))-2))

fout = file(outpath, 'w')     
# for line in output:
fout.write(output)
fout.close()