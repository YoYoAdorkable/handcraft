#coding:utf-8

# The main program: m_start.py
# Date: 2015-12-24 
# Mail: yuhailong880106@gmail.com
# Features: Network Testing


from db_DAL import *
from m_alarm import *
from m_monit import *
from time import sleep
from requests.exceptions import HTTPError
import os,sys
import time
import re
import threading
import datetime
import requests
import json
import socket
import urllib
import codecs
import thread
import multiprocessing
import subprocess

###########################################Network Testing#############################################
# Start collecting ip address
def net_monit():
    DAL.clear_ip_alarm_results()  # clear ip alarm table
    ip = DAL.get_ip_adderss()
    if ip:
        iplist=[]
        for num in range(len(ip)):
            iplist.extend(ip[num]["ip"].split(' '))
    iplist = list(set(iplist))
    net_ping_process(iplist)    
#-----------------------------------------------------------------------------------------------------
# Second Configuring the number of processes
def net_ping_process(iplist):
    # Configuring the number of processes
    ip_list=[]
    if iplist:
        if len(iplist) > 30:
            process_number = 30
        else:
            process_number = len(iplist)

        pool = multiprocessing.Pool(processes=process_number)
        for ip in iplist:
            if ip not in ' ':
                if ':' in ip:
                    ip=ip.split(':')[0]
                ip_list.append(ip)
                ip_list = list(set(ip_list))
        for ip in ip_list:
            pool.apply_async(net_ping_ip,(ip,))   # Sending a single ip
        pool.close()
        pool.join()
#-----------------------------------------------------------------------------------------------------
# Third detection ip connectivity
def net_ping_ip(ip):
    if subprocess.call('ping -c 5 -W 5 %s > /dev/null' % ip, shell=True) == 0:
        print '%s is OK' % ip
        net_ping_storage(ip,1) # Send monitoring results
    else:
        print '%s is DOWN' % ip
        count=1
        while 1:  # Loop detection 3 times
            if subprocess.call('ping -c 5 -W 5 %s > /dev/null' % ip, shell=True) == 0:
                print '%s is OK' % ip
                net_ping_storage(ip,1) # Send monitoring results
                break
            else:
                print '%s is DOWN' % ip
                count+=1

            if count == 3:
                net_ping_storage(ip,0) # Send monitoring results
                break
#-----------------------------------------------------------------------------------------------------
# Fourth ip network state storage
def net_ping_storage(ip,status):
    state = DAL.get_ip_results(ip)
    if state:
        if int(state[0]["status"]) != int(status):
            names = DAL.get_name_info(ip)
            name = ''
            for num in range(len(names)):
                numname = names[num]['name']
                name = name+str(numname)+' '
            DAL.update_ip_results(ip,status,name)
            if int(status) == 0:
                ip_alarm_storage(ip,0)
            else:
                ip_alarm_storage(ip,1)
    else:
        names = DAL.get_name_info(ip)
        name = ''
        for num in range(len(names)):
            numname = names[num]["name"]
            name = name+str(numname)+' '
        DAL.insert_ip_results(ip,status,name)
        if status == 0:
            ip_alarm_storage(ip,0)
#-----------------------------------------------------------------------------------------------------
# Fifth ip alarm state storage
def ip_alarm_storage(ip,status):
    DAL.insert_ip_alarm_results(ip,status)

#-----------------------------------------------------------------------------------------------------
########################################END Network Testing###########################################

########################################Time control center###########################################

# Time control
def time_control():
    hour = datetime.datetime.now().strftime('%H')
    minute = datetime.datetime.now().strftime('%M')
    
    if int(hour) >= 7 and int(hour) <= 22:
        num = int(minute)/5
        if num >= 0 or int(minute) < 1:
            return 1
        else:
            return 0
    else:
        if int(minute) == 30 or int(minute) < 1:
            return 1
        else:
            return 0
    
########################################Time control center###########################################

if __name__ == '__main__':
        print (time.strftime("%Y/%m/%d %H:%M:%S"))
        reload(sys)
        sys.setdefaultencoding('utf-8')

        time=time_control()
        if time == 1:
            net_monit()                 # Network Monitoring
            WEBMONIT.start()            # Business Monitor

            ALARM.ip_alarm()
            ALARM.web_alarm()
