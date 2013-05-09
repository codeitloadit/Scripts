import warnings
warnings.filterwarnings(action="ignore")
import csv
import os
import subprocess
import zipfile
subprocess.call('clear', shell=True)
print '\nInitializing AES Proofer...\n'

newsletter_names = list()

order_folder = raw_input('Order Directory: ')

# Get the proof file.
proof_file = None
proof_folder = os.path.join(order_folder, 'proof')
for root, dirs, files in os.walk(proof_folder):
    for f in files:
        if 'proof' in f.lower() and '.csv' in f.lower():
            proof_file = os.path.join(proof_folder, f)
            break
proof_reader = csv.reader(open(proof_file), delimiter = ',', skipinitialspace=True)
for i, line in enumerate(proof_reader):
    if i == 0: # Skip header line.
        continue

    if line[50]:
        newsletter_names.append(line[50])

# Find the documents folder.
documents_folder = os.path.join(order_folder, '../00 - documents')
if not os.path.exists(documents_folder):
    documents_folder = os.path.join(order_folder, 'documents')

# Create the zip file and add the proof file.
output_zip = zipfile.ZipFile(proof_folder + '/' + os.path.split(order_folder)[-1] + '_r0_proof.zip', 'w')
output_zip.write(proof_file, os.path.split(proof_file)[-1])

# Add the required newsletters to the zip file.
for root, dirs, files in os.walk(documents_folder):
    for f in files:
        for n in newsletter_names:
            if n.lower() in f.lower():
                output_zip.write(os.path.join(documents_folder, f), f)
