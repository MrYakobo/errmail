#!/usr/bin/python3

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import argparse

parser = argparse.ArgumentParser(description='Send a mail. Body should be passed on stdin. Make sure to populate the following envvars: SMTP_EMAIL: the sending email-address. SENDER_NAME: is added to the From header. SMTP_PASSWORD: your SMTP password. SMTP_URL: the url to the SMTP server')
parser.add_argument('--to', type=str, required=True, help='Recipident of the mail.')
parser.add_argument('--subject', type=str, required=True, help='Subject of the mail.', default='oops')

args = parser.parse_args()

if sys.stdin.isatty():
    raise Exception('pass the body on stdin')

msg = sys.stdin.read()

sender_email = os.environ["SMTP_EMAIL"]
password = os.environ['SMTP_PASSWORD']
sender_name = os.environ["SENDER_NAME"]
smtp_url = os.environ["SMTP_URL"]

receiver_email = args.to

message = MIMEMultipart("alternative")
message["Subject"] = args.subject
message["From"] = f'{sender_name} <{sender_email}>'
message["To"] = receiver_email

message.attach(MIMEText(msg, "html"))

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_url, 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
