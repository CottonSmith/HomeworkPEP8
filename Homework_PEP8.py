import email
import smtplib
import imaplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

GMAIL_SMTP = 'smtp.gmail.com'
GMAIL_IMAP = 'imap.gmail.com'

class EmailUser:
    def __init__(self,
                 login='login@gmail.com',
                 password='qwerty'):
        self.login = login
        self.password = password

    def send_message(self,
                     recipients=['vasya@email.com', 'petya@email.com'],
                     message_text='Message',
                     subject='Subject'):
        message = MIMEMultipart()
        message['From'] = self.login
        message['To'] = ', '.join(recipients)
        message['Subject'] = subject
        message.attach(MIMEText(message_text))
        myself = smtplib.SMTP(GMAIL_SMTP, 587)
        myself.ehlo()
        myself.starttls()
        myself.ehlo()
        myself.login(self.login, self.password)
        myself.sendmail(self.login, myself, message.as_string())
        myself.quit()

    def recieve_message(self, header = None):
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select('inbox"')
        if header:
            criterion = f'HEADER Subject {header}'
        else:
            criterion = 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()


if ne