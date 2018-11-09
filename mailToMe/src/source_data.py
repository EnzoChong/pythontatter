# -*- coding:utf-8 -*-
#!/usr/bin/env python

import MySQLdb
import sys
import os
from datetime import datetime, date, timedelta
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

root = os.path.dirname(os.path.realpath(__file__)) + '/..'

import simple_log as logger
sys.path.append(root + "/" + "conf")
import db_conf
import log_conf
import mail_conf
import html_page

def search_data():
    try:
        db = MySQLdb.connect(db_conf.db_host, db_conf.db_user, db_conf.db_password, db_conf.db_database_name)
    except Exception as e:
        logger.error("Connect to database fail." + str(e))
        return
    logger.notice("Connect to database success.")
    cursor = db.cursor()
    search_sql = "SELECT {} FROM {} WHERE date='{}'"
    yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    try:
        cursor.execute(search_sql.format('*', db_conf.db_table_name, yesterday))
    except Exception as e:
        logger.error("Execute sql instruction fail." + str(e))
        return
    results = cursor.fetchall()
    db.close()
    if len(results) != 0:
        logger.notice("Search data success. Total : " + str(len(results)))
        return results
    else:
        logger.notice("Search data fail, no data in datebase by search key date = '" + yesterday +  "'")
        return

def get_html():
    data = search_data()
    if data == None:
        return None
    cnt = len(data)
    disk_total = 0
    disk_used_total = 0
    disk_used_rate_total = 0
    disk_used_max = 0
    disk_used_max_time = ''
    disk_used_min = 0
    disk_used_min_time = ''
    cpu_load_total = 0
    cpu_load_max = 0
    cpu_load_max_time = ''
    cpu_load_min = 0
    cou_load_min_time = ''
    thread_count_total = 0
    thread_count_max = 0
    thread_count_max_time = ''
    thread_count_min = 0
    thread_count_min_time = ''
    memory_total = 0
    memory_used_total = 0
    memory_used_rate_total = 0
    memory_used_max = 0
    memory_used_max_time = ''
    memory_used_min = 0
    memory_used_min_time = ''
    for d in data:
        disk_total += d[2]
        disk_used_total += d[3]
        disk_used_rate_total += d[4]
        if disk_used_max < d[3]:
            disk_used_max = d[3]
            disk_used_max_time = d[1]
        if disk_used_min == 0 or disk_used_min > d[3]:
            disk_used_min = d[3]
            disk_used_min_time = d[1]
        cpu_load_total += d[7]
        if cpu_load_max < d[5]:
            cpu_load_max = d[5]
            cpu_load_max_time = d[1]
        if cpu_load_min == 0 or cpu_load_min > d[5]:
            cpu_load_min = d[5]
            cpu_load_min_time = d[1]
        thread_count_total += d[8]
        if thread_count_max < d[8]:
            thread_count_max += d[8]
            thread_count_max_time = d[1]
        if thread_count_min == 0 or thread_count_min > d[8]:
            thread_count_min = d[8]
            thread_count_min_time = d[1]
        memory_total += d[9]
        memory_used_total += d[10]
        memory_used_rate_total += d[11]
        if memory_used_max < d[10]:
            memory_used_max = d[10]
            memory_used_max_time = d[1]
        if memory_used_min == 0 or memory_used_min > d[10]:
            memory_used_min = d[10]
            memory_used_min_time = d[1]
    disk_space = str(round(disk_total / (cnt * 1024), 2)) + "GB"
    disk_used_space = str(round(disk_used_total / cnt, 2)) + "MB"
    disk_used_rate = str(round(disk_used_rate_total / cnt, 2)) + "%"
    cpu_core = '1核'
    cpu_load = str(round(cpu_load_total / cnt, 2))
    thread_count = str(thread_count_total / cnt)
    memory_space = str(round(memory_total / (cnt * 1024), 2)) + "GB"
    memory_used_space = str(round(memory_used_total / cnt, 2)) + "MB"
    memory_used_rate = str(round(memory_used_rate_total / cnt, 2)) + "%"

    return html_page.page.format(cpu_core, memory_space, disk_space, 
            cpu_load, cpu_load_max, cpu_load_max_time, cpu_load_min, cpu_load_min_time,
            thread_count, thread_count_max, thread_count_max_time, thread_count_min, thread_count_min_time,
            memory_used_space, memory_used_max, memory_used_max_time, memory_used_min, memory_used_min_time,
            disk_used_space, disk_used_max, disk_used_max_time, disk_used_min, disk_used_min_time)

def send_mail(page):
    yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    msg = MIMEText(page, 'html', 'utf-8')
    msg['From'] = formataddr(["server watcher", mail_conf.sender])
    msg['To'] = formataddr(["XueYuan, He", mail_conf.receiver])
    msg['Subject'] = yesterday + '服务器资源监控'

    try:
        server = smtplib.SMTP_SSL(mail_conf.host, mail_conf.host_port)
        server.login(mail_conf.sender, mail_conf.passwd)
        server.sendmail(mail_conf.sender, [mail_conf.receiver,], msg.as_string())
        server.quit()
        logger.notice("Send mail success.")
    except Exception as e:
        logger.error("Send mail fail." + str(e))
        return

if __name__ == '__main__':
    logger.init(root + '/' + log_conf.log_path, log_conf.log_name, log_conf.log_level)
    page = get_html()
    if page is not None:
        send_mail(page)
