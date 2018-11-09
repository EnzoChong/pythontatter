# -*- coding:utf8 -*_
#!/usr/bin/env python

import sys
import os
import time
import statvfs
import MySQLdb

import simple_log as logger

root = os.path.dirname(os.path.realpath(__file__)) + '/..'
sys.path.append(root + "/" + "conf")
import db_conf
import log_conf

def memory_stat():
    mem = {}
    f = open("/proc/meminfo")
    lines = f.readlines()
    f.close()
    for line in lines:
        if len(line) < 2: continue
        name = line.split(':')[0]
        var = line.split(':')[1].split()[0]
        mem[name] = long(var) * 1024.0
    mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
    return mem

def hdisk_stat():
    hdisk = {}
    rootPoint = os.statvfs('/')
    homePoint = os.statvfs('/home')
    hdisk['root_space_mb'] = (rootPoint.f_blocks * 4 / 1024)
    hdisk['root_used_mb'] = (rootPoint.f_blocks - rootPoint.f_bfree) * 4 / 1024
    hdisk['home_space_mb'] = (homePoint.f_blocks * 4 / 1024)
    hdisk['home_used_mb'] = (homePoint.f_blocks - homePoint.f_bfree) * 4 / 1024
    return hdisk

def load_stat():
    loadavg = {}
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()
    loadavg['lavg_1']=con[0]
    loadavg['lavg_5']=con[1]
    loadavg['lavg_15']=con[2]
    _, loadavg['thread_cnt']=con[3].split('/')
    loadavg['last_pid']=con[4]
    return loadavg

def collect_info():
    values = {}
    now = time.time()
    date = time.strftime("%Y-%m-%d", time.localtime(now))
    nowtime = time.strftime("%H:%M:%S", time.localtime(now))
    values["date"] = date
    values["time"] = nowtime
    
    disk_info = hdisk_stat()
    values["disk_total"] = disk_info["root_space_mb"]
    values["disk_used"] = disk_info["root_used_mb"]
    values["disk_used_rate"] = round(disk_info["root_used_mb"] * 100 / disk_info["root_used_mb"])
    cpu_info = load_stat()
    values["cpu_load_1_min"] = cpu_info["lavg_1"]
    values["cpu_load_5_min"] = cpu_info["lavg_5"]
    values["cpu_load_15_min"] = cpu_info["lavg_15"]
    values["thread_count"] = cpu_info["thread_cnt"]
    memory_info = memory_stat()
    values["memory_total"] = round(memory_info["MemTotal"] / (1024 * 1024), 2)
    values["memory_used"] = round(memory_info["MemUsed"] / (1024 * 1024), 2)
    values["memory_used_rate"] = round((memory_info["MemUsed"] * 100 / memory_info["MemTotal"]), 2)
    return values

def insert_data():
    try:
        db = MySQLdb.connect(db_conf.db_host, db_conf.db_user, \
                db_conf.db_password, db_conf.db_database_name, charset='utf8')
    except Exception as e:
        logger.error("Connect to database fail.")
        return
    logger.notice("Connect to database success.")
    cursor = db.cursor()
    insert_sql = 'INSERT INTO {} ({}) VALUES({})'
    field_list = 'date, time, disk_total, disk_used, disk_used_rate, cpu_load_1_min, cpu_load_5_min, cpu_load_15_min, thread_count, memory_total, memory_used, memory_used_rate'
    data = collect_info()
    values = "'" + data["date"] + "', " + \
                "'" + data['time'] + "', " + \
                str(data["disk_total"]) + ', ' + \
                str(data["disk_used"]) + ', ' + \
                str(data["disk_used_rate"]) + ', ' + \
                str(data["cpu_load_1_min"]) + ', ' + \
                str(data["cpu_load_5_min"]) + ', ' + \
                str(data["cpu_load_15_min"]) + ', ' + \
                str(data["thread_count"]) + ', ' + \
                str(data["memory_total"]) + ', ' + \
                str(data["memory_used"]) + ', ' + \
                str(data["memory_used_rate"])
    sql = insert_sql.format(db_conf.db_table_name, field_list, values)
    try:
        cursor.execute(sql)
    except Exception as e:
        logger.error("Insert data to database fail.")
        return
    db.commit()
    search_sql = "SELECT * FROM {} WHERE date='{}' AND time='{}'"
    cursor.execute(search_sql.format(db_conf.db_table_name, data["date"], data["time"]))
    results = cursor.fetchall()
    if len(results) != 0:
        logger.notice("Insert data to database success.")
    else:
        logger.error("Insert data fail, no search data in database.")

if __name__ == '__main__':
    logger.init(root + '/' + log_conf.log_path, log_conf.log_name, log_conf.log_level)
    insert_data()
