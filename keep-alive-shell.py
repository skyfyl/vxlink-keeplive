# -*- coding: UTF-8 -*-

import subprocess
import commands
import logging
import schedule
import time
import sys

from configparser import ConfigParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def run(user,pwd, keep_type, ids,server ,serverpwd):
    for id in ids:
        
        child = subprocess.Popen('sslocal -s {} -p {} -l 1081 -k {} -m aes-256-cfb'.format(server, id, serverpwd), stdout=subprocess.PIPE,shell=True)
        time.sleep(2)
        # a,b = commands.getstatusoutput('sslocal -s cn1.vxtrans.link -p {} -l 1081 -k YjFkNDg0NW -m aes-256-cfb -d start'.format(id))
        # print '退出状态: {}'.format(a)
        print '启动SS: cn1.vxtrans.link:{}'.format(id)
        
        child2 = subprocess.Popen('curl --socks5-hostname 127.0.1:1081 http://httpbin.org/ip',stdout=subprocess.PIPE, shell=True)
        proc_stdout = child2.communicate()[0].strip()
        # a,b = commands.getstatusoutput('curl --socks5-hostname 127.0.1:1081 http://httpbin.org/ip')
        # print '退出状态: {}'.format(a)
        print '查询iP: {}'.format(proc_stdout)

        # child3 = subprocess.Popen('sslocal -d stop', stdout=subprocess.PIPE, shell=True)
        child.terminate()
        
        # a,b = commands.getstatusoutput('sslocal -d stop')
        # print '退出状态: {}'.format(a)
        print '停止SS: cn1.vxtrans.link:{}'.format(id)

if __name__ == "__main__":
    cfg = ConfigParser()
    cfg.read('default.ini')
    user = cfg.get('login','user')
    pwd = cfg.get('login','pwd')
    ids = cfg.get('nodes','nodes_ids').split(',')
    on_time = str(cfg.get('time','keep_on_time'))
    off_time = str(cfg.get('time','keep_off_time'))
    server = str(cfg.get('server','ip'))
    serverpwd = str(cfg.get('server','pwd'))

    if sys.argv[1] == 'schedule':
        logging.info("start work, on time: {}, off time: {}".format(on_time, off_time))
        schedule.every().day.at(on_time).do(run, user= user,pwd=pwd, keep_type="keep_on", ids = ids, server=server, serverpwd=serverpwd)
        schedule.every().day.at(off_time).do(run, user= user,pwd=pwd, keep_type="keep_off", ids = ids, server=server, serverpwd=serverpwd)
        while True:
            schedule.run_pending()
            time.sleep(1)
    elif sys.argv[1] == 'run':
        run(user,pwd,'keep_on', ids, server,serverpwd)

    