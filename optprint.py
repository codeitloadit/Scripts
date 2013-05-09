import warnings
warnings.filterwarnings(action="ignore")
from pyPdf import PdfFileWriter, PdfFileReader
import csv
import os

PATH = r"/Users/Brian/Downloads"

INDEX_ASSOCIATION_KEY = 2
INDEX_NEWSLETTER_NAME = 50

previous_association_key = ''

work_orders = {}
newsletters = {}
work_orders_ref = [65]*99

order_number = raw_input('Enter the order number: ')

for root, dirs, files in os.walk(PATH):
    # Get the output csv file.
    for f in files:
        str_file = str(f).upper()
        if str_file.endswith('.CSV') and 'OUTPUT' in str_file:
            file_in = open(os.path.join(root, f))
            output_file = csv.reader(file_in, delimiter = ",", skipinitialspace=True) 
            break
    
    # Get the statements pdf file.
    for f in files:
        str_file = str(f).upper()
        if str_file.endswith('.PDF') and 'ASSESSMENTS' in str_file:
            pdf_name = os.path.join(root, str_file)
            statements_file = PdfFileReader(file(pdf_name)) 
            break
            
    key = ''
    headerline = output_file.next() # Skip headers.  
    for record_number, record in enumerate(output_file):
        newsletter_impressions = -1
        association_key = record[INDEX_ASSOCIATION_KEY]
        if association_key != previous_association_key: # New association found.
            new_association = True
            newsletter_name = record[INDEX_NEWSLETTER_NAME][:6]
            
            if newsletter_name:
                for f in files:
                    str_file = str(f).upper()
                    if str_file.endswith('.PDF') and newsletter_name in str_file:
                        pdf_name = os.path.join(root, str_file)
                        newsletter_file = PdfFileReader(file(pdf_name)) 
                        newsletter_impressions = newsletter_file.getNumPages()
                        break
                        
            else:   # Add it to statement onlies.
                newsletter_impressions = 0
                
            key = str(newsletter_impressions) + str(work_orders_ref[newsletter_impressions])
                
        else:
            new_association = False
        
        previous_association_key = association_key

        if not newsletter_impressions:
            if key not in work_orders:
                work_orders[key] = PdfFileWriter()           
            work_orders[key].addPage(statements_file.getPage(record_number))
        
        elif new_association:
            work_orders[key] = PdfFileWriter()
            work_orders_ref[newsletter_impressions] += 1
            work_orders[key].addPage(statements_file.getPage(record_number))
            
            newsletters[key] = PdfFileWriter()
            for page in range(int(newsletter_file.getNumPages())):
                newsletters[key].addPage(newsletter_file.getPage(page))
   
        else:
            work_orders[key].addPage(statements_file.getPage(record_number))
            
for k, v in work_orders.iteritems():
    tmpfout = file(str(os.path.join(PATH, 'tmp.pdf')), 'wb')
    work_orders[k].write(tmpfout)
    tmpfout.close()
    
    tmpfout = file(str(os.path.join(PATH, 'tmp.pdf')))
    tmpin = PdfFileReader(tmpfout)
    if int(k) >= 1000:
        fout = file(str(os.path.join(PATH, '{2} +{0} {1} ADDRESSES [{3}].pdf'.format(int(k[:2]), chr(int(k[2:])), order_number, tmpin.getNumPages()))), 'wb')
    else:
        fout = file(str(os.path.join(PATH, '{2} +{0} {1} ADDRESSES [{3}].pdf'.format(int(k[:1]), chr(int(k[1:])), order_number, tmpin.getNumPages()))), 'wb')
    work_orders[k].write(fout)
    fout.close()
    
    tmpfout.close()
    os.remove(os.path.join(PATH, 'tmp.pdf'))

    
       
for k, v in newsletters.iteritems():
    if int(k) >= 1000:
        fout = file(str(os.path.join(PATH, '{2} +{0} {1} CONTENTS.pdf'.format(int(k[:2]), chr(int(k[2:])), order_number))), 'wb')
    else:
        fout = file(str(os.path.join(PATH, '{2} +{0} {1} CONTENTS.pdf'.format(int(k[:1]), chr(int(k[1:])), order_number))), 'wb')
    newsletters[k].write(fout)
    fout.close()

    
    