from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
#from smtplib import SMTP_SSL as SMTP
from smtplib import SMTP

# Setup Email:
emailFrom = 'brian@optimaloutsource.com'
emailTo = 'brian@optimaloutsource.com'
emailSubject = 'Monthly HOA Assessment Dues Statement'
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
pdf.set_payload(open('/Users/brian/Downloads/test.pdf', 'rb').read())
Encoders.encode_base64(pdf)
pdf.add_header('Content-Disposition', 'attachment; filename="Assessment.pdf"')
msg.attach(pdf)

# SMTP Server Info:
serverAddress = 'smtp.gmail.com'
serverPort = 587
serverUser = 'brian@optimaloutsource.com'
serverPassword = '1qaz2wsx'

# Send email:
smtp = SMTP(serverAddress, serverPort)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login(serverUser, serverPassword)
smtp.sendmail(emailFrom, emailTo, msg.as_string())
smtp.close()


