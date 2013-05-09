 # certool.py


import warnings
warnings.filterwarnings(action="ignore")
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from os.path import join
import xlrd
import shutil
import copy
import zipfile
import sys
import subprocess
from settings import WORKING_DIRECTORY, RESOURCE_DIRECTORY

# Store OS and Directoy Separator
if os.name == 'posix':
    os_windows = False
    dir_sep = r'/'
    subprocess.call('clear', shell=True)
	
else:
    os_windows = True
    dir_sep = '\\'
    subprocess.call('cls', shell=True)

data_dir = 'data'
doc_dir = 'documents'

SUMMARY = '\n\nCertified Tool Summary\n\n'

final_headers = [
	'First Names',
	'Other Owner',
	'Address 1',
	'Address 2',
	'City',
	'State',
	'Zip',
	'Acct',
]

split_headers = [
	'First Names',
	'Address 1',
	'Acct',
]
            
for root, dirs, list_of_files in os.walk(WORKING_DIRECTORY):
    for ff in list_of_files:
        if (str(ff).endswith('.xls')):
            work_order = root.split(dir_sep)[len(root.split(dir_sep)) - 2]
            print 'Processing ' + work_order
            
            # Hacky, for now...
            summary_txt_file = open(root.replace(data_dir, work_order + '_summary.txt'))
            if (summary_txt_file.read().find('ACS') > 0):
                customer = 'ACS'
            else:
                customer = 'Camco Nevada'
            summary_txt_file.close()

            pdf_name_with_ext = pdf_name_only = None
            # Find the related PDF.
            pdf_folder = root.replace(data_dir, doc_dir)
            for sub_root, sub_dirs, sub_list_of_files in os.walk(pdf_folder + dir_sep):
                for f in sub_list_of_files:
                    if (str(f).endswith('.pdf')):
                        pdf_name_with_ext = str(f)
                        pdf_name_only = str(f).replace('.pdf','')

            data_file_name = str(ff).replace('.xls','')
            xls_workbook = xlrd.open_workbook(join(root, ff))
            xls_sheet = xls_workbook.sheet_by_index(0)
            input_stream = file(join(pdf_folder, pdf_name_with_ext), 'rb')
            pdf_input = PdfFileReader(input_stream)

            certified_folder = join(root.replace(dir_sep + data_dir,''), 'CERTIFED MAIL' + dir_sep)
            whitemail_folder = join(root.replace(dir_sep + data_dir,''), 'WHITE MAIL' + dir_sep)
            working_folder = join(root.replace(dir_sep + data_dir,''), 'WORKING' + dir_sep)

            os.mkdir(certified_folder); os.mkdir(whitemail_folder)

            # Remove empty rows from end of XLS.
            empty_rows = 0
            for row in range(xls_sheet.nrows):
                r = ''
                for col in range(xls_sheet.ncols): 
                    r += str(xls_sheet.cell(row,col).value)
                if len(r) < 10 :
                    empty_rows += 1
            
            raw_data = [['']*xls_sheet.ncols for _ in range(xls_sheet.nrows - empty_rows)]
            number_of_records = len(raw_data) - 1
            raw_string = ''; field_delimiter = ','; field_encloser = '"'
            index_of_first_address = index_of_second_address = index_of_account_number = -1
            index_of_first_names = index_of_other_owenrs = -1


            # Extract Association Name for Address Driver.
            address_driver_associations = [xls_sheet.ncols for _ in range(len(raw_data))]
            for row in range(len(address_driver_associations)):
                address_driver_associations[row] = str(xls_sheet.cell(row,0).value)            
            
            # Import formatted data to the 2D list.
            for row in range(len(raw_data)):
                for col in range(xls_sheet.ncols):                    
                    if (xls_sheet.cell(row,col).ctype == 2):
                        raw_data[row][col] = int(xls_sheet.cell(row,col).value)
                    else:
                        raw_data[row][col] = str(xls_sheet.cell(row,col).value)                            

            # Do various checks.
            for col in range(len(raw_data[0])):
                if (raw_data[0][col].strip() == 'OwnerName'):
                    index_of_first_names = col
                    
                if (raw_data[0][col].strip() == 'Address1'):
                    raw_data[0][col] = 'Address 1'
                if (raw_data[0][col].strip() == 'Address2'):
                    raw_data[0][col] = 'Address 2'
                if (raw_data[0][col].strip() == 'city'):
                    raw_data[0][col] = 'City'
                if (raw_data[0][col].strip() == 'state'):
                    raw_data[0][col] = 'State'
                if (raw_data[0][col].strip() == 'zip'):
                    raw_data[0][col] = 'Zip'
                    
                if (raw_data[0][col].strip() == 'Address 1'):
                    index_of_first_address = col
                if (raw_data[0][col].strip() == 'Address 1'):
                    index_of_first_address = col
                if (raw_data[0][col].strip() == 'Address 2'):
                    index_of_second_address = col
                    
                if (raw_data[0][col].strip() == 'Record Number'):
                    raw_data[0][col] = 'Acct'
                if (raw_data[0][col].strip() == 'Acct'):
                    index_of_account_number = col

            # Fix for new data format.
            if (index_of_first_names >= 0):
                for row in range(len(raw_data)):
                    if (row == 0):
                        raw_data[row].insert(0, 'First Names')
                        raw_data[row].insert(1, 'Other Owner')
                    else:
                        raw_data[row].insert(0, raw_data[row][index_of_first_names])
                        raw_data[row].insert(1, '') 
            
            # Add 'Address 2' if needed.
            if (index_of_second_address < 0):
                for row in range(len(raw_data)):
                    if (row == 0):
                        raw_data[row].insert(index_of_first_address + 1, 'Address 2')
                    else:
                        raw_data[row].insert(index_of_first_address + 1, '')

            # Add 'Acct' if needed.
            if (index_of_account_number < 0):
                for row in range(len(raw_data)):
                    if (row == 0):
                        raw_data[row].append('Acct')
                    else: #if not raw_data[row]:
                        raw_data[row].append("")

            # Now that all columns should exist, iterate through and remove the excess.
            for col in range(len(raw_data[0])):
                if (col < len(final_headers)):
                    while (raw_data[0][col].upper() != final_headers[col].upper()):
                        for row in range(len(raw_data)):
                            raw_data[row].pop(col)
                else:
                    if (col < len(raw_data[0])):
                        for row in range(len(raw_data)):
                            raw_data[row].pop(col)

            # Check for erroneous fields (State, Zip).
            for row in range(len(raw_data)):
                for col in range(len(raw_data[row])):
                    if (row > 0 and col == 6 and len(str(raw_data[row][col])) != 5):
                        if (len(str(raw_data[row][col])) == 4 and str(raw_data[row][col]).isdigit()):
                            raw_data[row][col] = '0' + str(raw_data[row][col])
                        else:
                            if (len(str(raw_data[row][col])) != 10 and str(raw_data[row][col]).count('-') != 1):
                                print 'Invalid Zip Code in ' + work_order + ' on row ' + str(row) \
                                    + ' with length of ' + str(len(str(raw_data[row][col]))) + ' and value of ' \
                                        + str(raw_data[row][col])

            # Create copy of data for Address Driver.
            address_driver_data = copy.deepcopy(raw_data)
            
            # Export 2D list to a string with CSV formatting.
            for row in range(len(raw_data)):
                for col in range(len(raw_data[row])):
                    if (col == len(raw_data[row]) - 1):
                        field_delimiter = '\n'
                    else:
                        field_delimiter = ','
                    raw_string += field_encloser + str(raw_data[row][col]) + field_encloser + field_delimiter

            # Write FINAL.csv file. <- OLD
            final_csv_file = open(certified_folder + data_file_name + '_FINAL_' + str(number_of_records) + '.csv' , 'w')
            final_csv_file.write(raw_string); final_csv_file.close()
            raw_string = ''

            # Determine the job type.
            if (pdf_name_with_ext.upper().find('MERGE') >= 0):
                is_mail_merge = True
            else:
                is_mail_merge = False

            # Depending on job type, generate output.
            if (not is_mail_merge):
                pod_size = 0
                temp_file = certified_folder + 'temp.pdf'
                temp_pdf = PdfFileWriter()
                blank_pdf = PdfFileReader(file(join(RESOURCE_DIRECTORY, 'BLANK.pdf'), 'rb'))

                # Copy the input pdf to the output.
                for page in range(int(pdf_input.getNumPages())):
                    temp_pdf.addPage(pdf_input.getPage(page))

                # Add a blank page if needed.
                if (pdf_input.getNumPages() % 2 != 0):
                    temp_pdf.addPage(blank_pdf.getPage(0))
                    
                # Write the temp to pdf.
                temp_stream = file(temp_file, 'wb')
                temp_pdf.write(temp_stream)
                temp_stream.close()
                input_stream.close()

                # Then remove input replace with temp.
                os.remove(join(pdf_folder, pdf_name_with_ext))
                pdf_name_with_ext = pdf_name_with_ext.replace('.pdf', '_' + str(pdf_input.getNumPages()) + '.pdf')
                os.rename(temp_file, certified_folder + work_order + '_' + pdf_name_with_ext)

                # Create a copy for White Mail folder.
                shutil.copyfile(certified_folder + work_order + '_' + pdf_name_with_ext, whitemail_folder + work_order \
                    + ' CONTENTS (+' + str(pdf_input.getNumPages()/2)+ ').pdf')

                # Move the xls to the White Mail folder.
                os.rename(join(root, ff), whitemail_folder + work_order + '_' + str(number_of_records) + '.xls')

            else:
                # Removed unwanted columns for SPLIT file.
                for col in range(len(raw_data[0])):
                    if (col < len(split_headers)):
                        while (raw_data[0][col] != split_headers[col]):
                            for row in range(len(raw_data)):
                                raw_data[row].pop(col)
                    else:
                        if (col < len(raw_data[0])):
                            for row in range(len(raw_data)):
                                raw_data[row].pop(col)

                # Export 2D list to a string with SPLIT file formatting.
                for row in range(len(raw_data)):
                    if (row == 0):
                        continue
                    for col in range(len(raw_data[row])):
                        if (col == len(raw_data[row]) - 1):
                            field_delimiter = '\n'
                        else:
                            field_delimiter = ''
                        raw_string += str(raw_data[row][col]) + field_delimiter

                raw_string = raw_string.replace(' ', '_').replace('.', '').replace(',', '').replace('"', '').replace('/', '')
                split_namelist = raw_string.split('\n')

                # Iterate through page(s) and generate separate files.
                pod_size = int(pdf_input.getNumPages()) / number_of_records
                record_number = 0

                output_zip_file = zipfile.ZipFile(certified_folder + pdf_name_only + '.zip', 'w')

                for page in range(int(pdf_input.getNumPages())):
                    if (page % pod_size == 0):
                        temp_pdf = PdfFileWriter()
                        record_number += 1
                        for sub_page in range(pod_size):
                            temp_pdf.addPage(pdf_input.getPage(page + sub_page))
                        sub_zip_name = join(root, split_namelist[record_number - 1] + '.pdf')
                        temp_stream = file(sub_zip_name, 'wb')
                        temp_pdf.write(temp_stream)
                        temp_stream.close()
                        output_zip_file.write(sub_zip_name, split_namelist[record_number-1] + '.pdf')
                        os.remove(sub_zip_name)

                input_stream.close()
                os.rename(join(pdf_folder, pdf_name_with_ext), whitemail_folder + work_order +  ' CONTENTS (+' \
                    + str(pdf_input.getNumPages()/number_of_records/2)+ ').pdf')

                # Move the xls to the White Mail folder.
                os.rename(join(root, ff), whitemail_folder + work_order + '_' + str(number_of_records) + '.xls')

            # Remove original folders and files.
            shutil.move(join(root.replace(data_dir,work_order + '_summary.txt')), root)
            shutil.move(join(root.replace(data_dir,work_order + '_summary.csv')), root)
            shutil.rmtree(root)
            shutil.rmtree(pdf_folder)

            #Create Address Driver.
            address_driver_temp_file = str(join(RESOURCE_DIRECTORY, 'TEMP.pdf'))
            address_driver_buffer_file = str(join(RESOURCE_DIRECTORY, 'DRIVER.pdf'))
            address_driver_buffer_stream = file(address_driver_temp_file, 'wb')
            address_driver_pdf = PdfFileWriter()

            for col in range(len(address_driver_associations)):
                if (col):
                    dX = 83.5
                    dY = 21
                    dH = 10
                    dMod = 1
                    c = canvas.Canvas(address_driver_buffer_file, pagesize=letter, bottomup = 0)
                    c.setFont("Helvetica", 9)
                    c.drawString(dX, dY + (dH * dMod), address_driver_associations[col]); dMod += 1
                    c.drawString(dX, dY + (dH * dMod), "C/O " + customer); dMod += 1
                    c.drawString(dX, dY + (dH * dMod), "P.O. BOX 12117"); dMod += 1
                    c.drawString(dX, dY + (dH * dMod), "Las Vegas, NV 89112-2117"); dMod += 8
                    dY = dY + 3
                    c.drawString(dX, dY + (dH * dMod), address_driver_data[col][0])
                    if (address_driver_data[col][0] is not ''):dMod += 1
                    c.drawString(dX, dY + (dH * dMod), address_driver_data[col][1])
                    if (address_driver_data[col][1] is not ''):dMod += 1
                    c.drawString(dX, dY + (dH * dMod), address_driver_data[col][2])
                    if (address_driver_data[col][2] is not ''):dMod += 1
                    c.drawString(dX, dY + (dH * dMod), address_driver_data[col][3])
                    if (address_driver_data[col][3] is not ''):dMod += 1
                    c.drawString(dX, dY + (dH * dMod), address_driver_data[col][4] + ', ' + address_driver_data[col][5] \
                        + ' ' + str(address_driver_data[col][6]))

                    c.showPage()
                    c.save()

                    final_pdf = PdfFileReader(file(address_driver_buffer_file, 'rb'))
                    address_driver_pdf.addPage(final_pdf.getPage(0))
                    address_driver_pdf.write(address_driver_buffer_stream)
            address_driver_buffer_stream.close()

            # Copy temp driver to White Mail folder.
            shutil.copyfile(address_driver_temp_file, whitemail_folder + work_order + ' ADDRESSES.pdf')
            
            # Create PRINT file.
            print_driver_addresses_stream = file(whitemail_folder + work_order + ' ADDRESSES.pdf', 'rb')
            print_driver_addresses_reader = PdfFileReader(print_driver_addresses_stream)
            if (not is_mail_merge):
                print_driver_contents_stream = file(whitemail_folder + work_order + ' CONTENTS (+' + \
                    str(pdf_input.getNumPages()/2)+ ').pdf', 'rb')
            else:
                print_driver_contents_stream = file(whitemail_folder + work_order +  ' CONTENTS (+' + \
                    str(pdf_input.getNumPages()/number_of_records/2)+ ').pdf', 'rb')
            print_driver_contents_reader = PdfFileReader(print_driver_contents_stream)

            final_print_pdf = PdfFileWriter()
            blank_pdf = PdfFileReader(file(join(RESOURCE_DIRECTORY, 'BLANK.pdf'), 'rb'))

            print_record_counts = 0
            print_impression_counts =  0

            # Copy the input pdf to the output.
            for record in range(int(print_driver_addresses_reader.getNumPages())):
                final_print_pdf.addPage(print_driver_addresses_reader.getPage(print_record_counts))
                print_impression_counts += 1
                if ((print_driver_contents_reader.getNumPages()/number_of_records) % 2 == 0) or \
                    (print_driver_contents_reader.getNumPages()/number_of_records == 1 and is_mail_merge is False):
                    final_print_pdf.addPage(blank_pdf.getPage(0))
                    print_impression_counts += 1
                if (not is_mail_merge):
                    for page in range(print_driver_contents_reader.getNumPages()):
                        final_print_pdf.addPage(print_driver_contents_reader.getPage(page))
                        print_impression_counts += 1
                else:
                    for page in range(print_driver_contents_reader.getNumPages()/number_of_records):
                        final_print_pdf.addPage(print_driver_contents_reader.getPage(page + \
                            (print_record_counts * pod_size)))
                        print_impression_counts += 1
                print_record_counts += 1

            
            final_print_file = whitemail_folder + work_order + ' PRINT [Count = ' + str(print_record_counts) + \
                ', Impressions = ' + str(print_impression_counts/print_record_counts) + '].pdf'
            
            sub_summary = copy.deepcopy(final_print_file)
            
            final_print_stream = file(final_print_file, 'wb')
            final_print_pdf.write(final_print_stream)
            final_print_stream.close()
            print_driver_addresses_stream.close()
            print_driver_contents_stream.close()

            shutil.move(final_print_file, final_print_file.replace(dir_sep + 'WHITE MAIL', ''))
            replace_string = (root + dir_sep + work_order + dir_sep + 'WHITE MAIL' + \
                dir_sep).replace(dir_sep + data_dir + dir_sep + work_order, '')

            SUMMARY = SUMMARY + sub_summary.replace(replace_string, '').replace(' PRINT', '').replace('.pdf','\n')
                                                                         
SUMMARY = SUMMARY + '\nComplete!\n'
print SUMMARY

if os_windows:
    exit = raw_input('Press Enter to exit.')
