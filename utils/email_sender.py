import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.generic_config import generic_config


class EmailSender():

    def __init__(self, sender, receiver, subject):
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = subject
        self.msg['From'] = sender
        self.msg['To'] = receiver
        self.server = smtplib.SMTP('smtp.zoho.com', 587)

    def create_email_content(self, html_template, plain_text = 'Hello from Stori Card'):
        part1 = MIMEText(plain_text, 'plain') 
        part2 = MIMEText(html_template, 'html')
        self.msg.attach(part1) 
        self.msg.attach(part2)

    def send_email(self):
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.msg['From'], generic_config['sender_email_password'])
        self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
        self.server.quit()