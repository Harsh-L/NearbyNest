import smtplib
import os
from email.mime.text import MIMEText

# The smtp.example.com here should be replaced with the actual name of the SMTP server you are using.
class Email_OTP():

    def sendOTPViaEmail(MailTo:str, OTP):
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = os.getenv('SMTP_PORT')
        
        smtp_user = os.getenv('SMTP_USER')
        smtp_password = os.getenv('SMTP_PASSWORD')

        smtp_connection = smtplib.SMTP(smtp_server,smtp_port)
        smtp_connection.starttls()
        smtp_connection.login(smtp_user, smtp_password)
        
        # email_body = f"Your One Time Password (OTP) is: \n\n {OTP}\n\nYour OTP will expire in 5 min.\nDo not share your OTP with anyone." # Plain - subtype
        email_body = f"Your One Time Password (OTP) is: <br><br> <b>{OTP}</b> <br><br>Your OTP will expire in 5 min. <br>Do not share your OTP with anyone." # html - subtype
        email_message = MIMEText(email_body,'html')

        email_message['Subject'] = 'Farm2U E-mail Verification'
        email_message['From'] = smtp_user
        email_message['To'] = MailTo
        # Send the email
        smtp_connection.sendmail(smtp_user, MailTo, email_message.as_string())
        # 4. Close the SMTP connection
        smtp_connection.quit()