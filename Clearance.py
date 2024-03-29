#!/usr/bin/python
#coding:utf-8
# python 3
# tested in Win

import smtplib, configparser, os ,sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders



confile = 'E:\\mail.ini'
# choice = 'KC2'
config = configparser.ConfigParser()
config.read(confile)

choice = input("Which place ?")
choice = choice.upper()


if choice == 'KC2' or choice == 'K':
    choice == 'KC2'
elif choice == 'NTT' or choice == 'N':
    choice == 'NTT'
else:
    print('Wrong input')
    sys.exit()



mailsvr = config['mailsvr']['mailsvr']
fromaddr = config[choice]['fromaddr']
toaddr = config[choice]['toaddr'].split(',')


body = config[choice]['body']
# print(body)
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)

msg['Subject'] = config[choice]['title']
msg.attach(MIMEText(body,'plain'))

if choice == 'KC2' or choice == 'K':
    choice == 'KC2'
    attach = config[choice]['attach']
    # print(attach)
    with open(attach,'rb') as fo:
        att = MIMEBase('application', "octet-stream")
        att.set_payload(fo.read())
    encoders.encode_base64(att)
    att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attach))
    msg.attach(att)

text = msg.as_string()

server = smtplib.SMTP(mailsvr)
server.ehlo()
# server.starttls()
server.sendmail(fromaddr,toaddr,text)

