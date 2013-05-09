import warnings
warnings.filterwarnings(action="ignore")
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from pyPdf import PdfFileWriter, PdfFileReader
#from smtplib import SMTP_SSL as SMTP
from smtplib import SMTP
import csv
import os
import subprocess
import sys
import time


TESTING = True
if raw_input('Do you want to send to homeowner? [no]: ') == 'yes':
    TESTING = False

subprocess.call('clear', shell=True)
print '\nInitializing E-Statement Mailer...\n'
PATH = r"/Users/Brian/Downloads"
PDFOUT = str(os.path.join(PATH, 'OUT.pdf'))
pdfFile = ''
csvFile = ''
customer = ''
    
for root, dirs, files in os.walk(PATH):
    for f in files:
        strFile = str(f)
        if strFile.upper().endswith('.PDF') and ('Statement' in strFile or 'Assessment' in strFile):
            pdfName = os.path.join(root, strFile)
            pdfFile = PdfFileReader(file(pdfName))            
        elif strFile.upper().endswith('.CSV') and 'Output' in strFile:
            csvFile = open(os.path.join(root, strFile)) 
            
            if strFile.count('CHI'):
                customer = 'CHI'
                has_backer = False
            elif strFile.count('CAMCO'):
                customer = 'CAMCO'
                has_backer = False
            elif strFile.count('Kuester'):
                customer = 'KUESTER'
                has_backer = False
            elif strFile.count('Cardinal'):
                customer = 'CARDINAL'
                has_backer = True
            if strFile.count('PMP'):
                customer = 'PMP'
                has_backer = False
            elif strFile.count('Progressive'):
                customer = 'PROGRESSIVE'
                has_backer = True
            else:     
                customer = raw_input('Enter customer:  ').upper()
                has_backer = False
                if raw_input('Do these statements have a backer? [y/n] ') == 'y':
                    has_backer = True
                
    if not pdfFile:
        print 'ERROR: Missing Assessments/Statement.pdf'    
    if not csvFile:
        print 'ERROR: Missing Output.csv'      
    if not pdfFile or not csvFile:
        print '\nExiting...\n'
        sys.exit()
       
reader = csv.reader(csvFile, delimiter = ",", skipinitialspace=True) 

recordCnt = 0
rowCnt = 1
for i, row in enumerate(reader):
    rowCnt += 1
    if recordCnt > 0:  # Skip headers
    
        # Extract customer name, email address and newsletter name.
        customerName = row[3].strip()
        emailTo = row[10].strip().replace(',', '.')
        nl_slug = ''
        if row[50]:
            nl_slug = row[50][0:6]
        
        # Valiate email address.
        if '@' not in emailTo or '.' not in emailTo:
            print 'Invalid email address:  ' + emailTo
            break
            
        print '{0}. Sending {1}'.format(i, emailTo)
        pdfOut = PdfFileWriter()
        if has_backer:
            pdfOut.addPage(pdfFile.getPage((i * 2) - 2))
            pdfOut.addPage(pdfFile.getPage((i * 2) - 1))
        else:
            pdfOut.addPage(pdfFile.getPage(i-1))
        
        nlPages = 0
        if nl_slug:
            nlFile = PdfFileReader(file(os.path.join(root, nl_slug + '_1.pdf'))) 
            nlPages = int(nlFile.getNumPages())
            for nlpg in range(int(nlFile.getNumPages())):
                pdfOut.addPage(nlFile.getPage(nlpg))                  
        fout = file(PDFOUT, 'wb')
        pdfOut.write(fout)
        fout.close()
        
        emailSubject = 'Monthly HOA Assessment Dues Statement'
        pdfFileName = 'Assessment'
        
        
        if TESTING:
            nlSubject = ''
            if nlPages:
                nlSubject = ' +' + str(nlPages)
            pdfFileName = customerName
            emailTo = 'brian@optimaloutsource.com'
            emailSubject = str(i) + ': Monthly HOA Assessment Dues Statement - TEST' + nlSubject

        
        # Setup Email:
        serverAddress = 'mail.opt-e-mail.com'
        serverPort = 25
        
        emailBcc = ''
        
        if customer == 'CHI':
            emailFrom = 'chi@mail.opt-e-mail.com'
            serverUser = 'chi'
            serverPassword = 'optimal'
#             emailBcc = 'joshm@optimaloutsource.com'
            
        if customer == 'CAMCO':
            emailFrom = 'camconv@mail.opt-e-mail.com'
            serverUser = 'camconv'
            serverPassword = '7XPPm8U'
#             emailBcc = 'sebouh@optimaloutsource.com'
            
        if customer == 'KUESTER':
            emailFrom = 'kuester@mail.opt-e-mail.com'
            serverUser = 'kuester'
            serverPassword = 'MtH34kf'
            emailBcc = 'joshm@optimaloutsource.com'

        if customer == 'CARDINAL':
            emailFrom = 'cardinalpm@mail.opt-e-mail.com'
            serverUser = 'cardinalpm'
            serverPassword = 'cpm2010'
            emailBcc = 'chase@optimaloutsource.com'

        if customer == 'PMP':
            emailFrom = 'pmprofessionals@mail.opt-e-mail.com'
            serverUser = 'pmprofessionals'
            serverPassword = '3djAru2Y'
#             emailBcc = 'sebouh@optimaloutsource.com'
            
        if customer == 'PROGRESSIVE':
            emailFrom = 'progressive@mail.opt-e-mail.com'
            serverUser = 'progressive'
            serverPassword = 'pro8re55ive'
#             emailBcc = 'chase@optimaloutsource.com'

        emailType = 'plain'
        emailBody = """\
Attached is your Monthly Homeowners Assessment statement from your homeowners association.


The letter is in Adobe PDF format. If you need a reader, simply click the link below.

http://www.adobe.com/products/acrobat/readstep.html


        """
        
        # Setup headers:
        msg = MIMEMultipart()
        msg['From'] = emailFrom
        msg['To'] = emailTo
        msg['Subject'] = emailSubject
        msg.attach(MIMEText(emailBody, emailType))
        
        # Setup PDF attachment(s):
        pdf = MIMEBase('application', 'pdf')
        pdf.set_payload(open(PDFOUT, 'rb').read())
        Encoders.encode_base64(pdf)
        pdf.add_header('Content-Disposition', 'attachment; filename="' + pdfFileName + '.pdf"')        
        msg.attach(pdf)                
        
        # Send email:
        smtp = SMTP(serverAddress, serverPort)
        smtp.login(serverUser, serverPassword)
        finalTo = [emailTo, emailBcc]
        smtp.sendmail(emailFrom, finalTo, msg.as_string())
        smtp.close()   
                
    recordCnt += 1
#     time.sleep(1)

print '\nSent ' + str(recordCnt-1) + ' records out of ' + str(rowCnt-2) + ' total.\n'

subprocess.call('rm ' + PDFOUT, shell=True)
            
