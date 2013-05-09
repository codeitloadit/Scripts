import warnings
warnings.filterwarnings(action="ignore")
import csv
import os

newsletter_directory_path = raw_input('Path to newsletter folder:\n')
output_file_path = raw_input('Path to output file:\n')

directory_file_names = list()
output_file_names = list()
missing_newsletters = list()

for root, dirs, files in os.walk(newsletter_directory_path):
    for f in files:
        if str(f).endswith('.tif'):
            directory_file_names.append(str(f))

fin = open(output_file_path)
output_file = fin.readlines()
fin.close()

output_reader = csv.reader(output_file, delimiter = ',', skipinitialspace=True)
output_reader.next()

for line in output_reader:
    newsletter_name = line[50].replace('XX.jpg', '01.tif')
    if newsletter_name and newsletter_name not in output_file_names:
        output_file_names.append(newsletter_name)

for newsletter in output_file_names:
    if newsletter not in directory_file_names:
        missing_newsletters.append(newsletter)

if missing_newsletters:
    print '\n\nMissing {0} Newsletter(s):\n'.format(len(missing_newsletters))

    for newsletter in missing_newsletters:
        print '\t' + newsletter.replace('01.tif', 'XX.tif')

    print '\n\n'

else:
    print '\n\nNo Missing Newsletters!\n\n'
