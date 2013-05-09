import warnings
warnings.filterwarnings(action="ignore")
import os
import subprocess
subprocess.call('clear', shell=True)
print '\nInitializing CSV Merger...\n'

working_dir = r'/Users/Brian/Downloads'
    
file_cnt = 0
row_cnt = 0
headers = ''
has_headers = False
fout = open(os.path.join(working_dir, 'MERGED_CSV.csv'),"a")

for root, dirs, files in os.walk(working_dir):
    for f in files:
        if not str(f).endswith('MERGED_CSV.csv') and not str(f).startswith('.'):
            file_cnt += 1
            print '{0}. Merging {1}'.format(file_cnt, f)
            for i, line in enumerate(open(os.path.join(root, str(f)))):
                if file_cnt == 1 and i == 0:
                    headers = line
                    
                if file_cnt > 1 and i == 0 and line == headers:
                    has_headers = True
                else:
                    fout.write(line.replace('\r\r\n', '').replace('\r', '\n').replace('\n\n', '\n'))
                    row_cnt += 1
                
fout.close()      
print '\n\nCSV Merger Summary:'
print '\tFiles Merged:\t{0}'.format(file_cnt)
print '\tTotal Rows:\t{0}'.format(row_cnt)
print '\tWith headers:\t{0}'.format(has_headers)
print '\n'
