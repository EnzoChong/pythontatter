# -*- coding:utf-8 -*-
#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import sys
import os

workroot = os.path.dirname(os.path.realpath(__file__)) + "/../"

sys.path.append(workroot + ".")
import simple_log as logger

sys.path.append(workroot + "conf")
import mail_conf as conf

def send_mail(subject, content):
    msg = MIMEText(content, conf.content_type, conf.charset)
    msg['From'] = formataddr([conf.send_name, conf.sender_addr])
    msg['To'] = formataddr([conf.receiver_name, conf.receiver_addr])
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP_SSL(conf.host, conf.host_port)
        server.login(conf.sender_addr, conf.passwd)
        server.sendmail(conf.sender_addr, [conf.receiver_addr,], msg.as_string())
        server.quit()
        logger.notice("Send mail success.")
    except Exception as e:
        logger.error("Send mail fail." + str(e))

if __name__ == '__main__':
    print "ok"
