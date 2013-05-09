import warnings
warnings.filterwarnings(action="ignore")
import csv
import os

working_dir = raw_input('Path to order root:\n')
nlist = list()
lout = list()

print_on_back = False
if raw_input('Can newsletter be printed on the back of the statements? [y/n] ') == 'y':
    print_on_back = True

def sort_it(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

newsletter_directory = os.path.join(working_dir, 'documents')
if not os.path.exists(newsletter_directory):
    newsletter_directory = os.path.join(working_dir, '../00 - documents')

fin = open(os.path.join(newsletter_directory, 'manifest.csv'))
manifest = fin.readlines()
fin.close()

for root, dirs, files in os.walk(newsletter_directory):
    for f in files:
        fname = str(f).upper()
        if fname.endswith('.TIF'):
            nlist.append(fname)
            
nlist.sort(reverse=True)
oldname = ''
for name in nlist:
    if name[:6] != oldname[:6]:
        oldname = name
        for line in manifest:
            if name[:6] in line:
                lout.append(line.split(',')[0] + ',' + name[6:8].strip('0'))

lout.sort()
lout = sort_it(lout)

for line in lout:
    print line
    
counts = ''
CSVOUT = ''
for root, dirs, files in os.walk(working_dir + '/data'):
    for f in files:
        if str(f).endswith('Counts.csv'):
            CSVOUT = str(os.path.join(working_dir, str(f).replace('.csv', ' with Newsletters.csv')))
            fin = open(os.path.join(root, f))
            counts = fin.readlines()
            fin.close()
            break
   
counts_reader = csv.reader(counts, delimiter = ',', skipinitialspace=True)

cout = list()   
header = True  
for row in counts_reader:
    if header:
        row[0] = row[0].replace('\xef\xbb\xbf', '')
        row.append('Newsletters')
        cout.append(row)
        header = False
        continue
        
    match = False
    for count in lout:
        assoc = count.split(',')[0]
        cnt = count.split(',')[1]
        
        if print_on_back and cnt == '1':
            cnt = 0
        elif int(cnt) % 2 == 0:
            cnt = str(int(cnt) / 2)
        else:
            cnt = str((int(cnt) + 1) / 2)
            
        if row.count(assoc):
            row[-1] = str(cnt)
            cout.append(row)
            match = True
            break
            
    if not match:
        row[-1] = '0'
        cout.append(row)
        

fout = file(CSVOUT, 'w')     
for line in cout:
    row = ''
    for field in line:
        row += field + ','
    fout.write(row + '\n')
fout.close()
            

print '\n\nFinished!\n\n'



