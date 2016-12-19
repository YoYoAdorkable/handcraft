# -*- coding:utf-8 -*-

# The main program: m_monit.py
# Date: 2015-12-30
# Mail: yuhailong880106@gmail.com
# Features: Web Url mointor



from db_DAL import *
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

reload(sys)
sys.setdefaultencoding('utf-8')

g_mutex=threading.Condition()
g_pages=[]  #获取所有url地址
g_queueURL=[]   #等待分析url列表
g_existURL=[]   #已经分析列表
g_failedURL=[]  #分析失败列表
g_totalcount=0 #分析过的数字




class detect:
    def __init__(self,detectname,taskUrl,threadnum):                                # We will get the information into the self
        self.detectname=detectname
        self.taskUrl=taskUrl
        self.threadnum=threadnum
        self.threadpool=[]
        self.tect()

    
    def tect(self):
        global g_queueURL
        for num in range(len(self.taskUrl)):                                        # The information stored in the global g_queueURL list
            if int(self.taskUrl[num]["rule"]) == 1:
                ips = ''
                for ip in self.taskUrl[num]["ip"].split(' '):
                    self.taskUrl[num]["ip"] = ''
                    if ip:
                        if ":" in ip:
                            ip_input=ip.split(':')[0]
                            status = DAL.get_ip_results(ip_input)
                        else:
                            status = DAL.get_ip_results(ip)
                        if int(status[0]["status"]) == 1:
                            ips = ips+' '+ip
                self.taskUrl[num]["ip"] = ips.lstrip()
                if self.taskUrl[num]["ip"]:
                    g_queueURL.append(self.taskUrl[num])

        print self.detectname+" 启动..."
        while(len(g_queueURL)!=0):                                                  # g_queueURL list is not empty start detecting
            print 'Searching depth '
            self.detectAll()


    def detectAll(self):
        global g_queueURL
        global g_totalcount
        global lock
        i=0
        while i<len(g_queueURL):                                                    # g_queueURL list not empty
            j=0
            while j<self.threadnum and i+j < len(g_queueURL):                       # Open Thread
                g_totalcount+=1
                threadresult=self.detectGeturl(g_queueURL[i+j],j)                   # Single message read out to detectGeturl execution 
                if threadresult != None:
                    print 'Thread started:',i+j,'--File number =',g_totalcount
                j+=1
            i+=j
        g_queueURL=[]


    def detectGeturl(self,monit_info,tid):                                          # Data is sent to DetectThread
        detecthread=DetectThread(monit_info,tid)
        self.threadpool.append(detecthread)
        detecthread.setDaemon(True)
        detecthread.start()
        detecthread.stop()
        detecthread.join(60)


class DetectThread(threading.Thread):                                               # Start url monitor
    def __init__(self,monit_info,tid):
        threading.Thread.__init__(self)
        self.monit_info=monit_info
        self.tid=tid

    def run(self):
        global g_mutex
        global g_failedURL
        global g_queueURL

        count=0

        send_headers = {
            'Host':self.monit_info['header'],
            'User-Agent':'kuyun_monit/v2 (mail:ops@kuyun.com)',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection':'keep-alive'
        }
        url = ''
        for ip in self.monit_info["ip"].split(' '):                                                   # Replace ip domain
            url = str(self.monit_info["url"]).replace(self.monit_info["header"],ip)
            count=0
            try:
                req = requests.get(url,headers=send_headers,timeout=7)                                 # Analysis url, timeout 7 seconds, a timeout or other exception will retry 3 times, wait 5 seconds
                req.raise_for_status()
                html=req.content
                code=str(req.status_code)
                times=round(float(req.elapsed.microseconds)/1000/1000,2)
                self.analy(self.monit_info,url,ip,html)                                                # Detecting normal, into the analy see if it needs to send an alarm function
                print self.monit_info['name'],'-',ip,code,times
            except Exception,e:
                print self.monit_info['name'],Exception,":",str(e)
                count+=1
                times='第 %d 次超时' %count
                name = ''
                name = self.monit_info["name"]+'_'+ip
                header = self.monit_info["header"]
                self.log(name,url,str(e),times,header)                                                         # Error information is written to the log 

                time.sleep(5)
                while 1:
                    try:
                        req = requests.get(url,headers=send_headers,timeout=7)
                        req.raise_for_status()
                        html=req.content
                        code=str(req.status_code)
                        times=round(float(req.elapsed.microseconds)/1000/1000,2)
                        self.analy(self.monit_info,url,ip,html)
                        break
                    except Exception,e:
                        print self.monit_info['name'],Exception,":",str(e)
                        count+=1
                        times='第 %d 次超时' %count
                        name = ''
                        name = self.monit_info["name"]+'_'+ip
                        header = self.monit_info["header"]
                        self.log(name,url,str(e),times,header)
                        time.sleep(5)

                    if count == 3:
                        information=str(e)
                        self.patrol_wrong(self.monit_info,url,ip,information)
                        break


        g_mutex.acquire()
        g_existURL.append(self.monit_info['url'])

    def analy(self,monit_info,url,ip,html):
        date = datetime.datetime.now()
        date=date.strftime('%Y-%m-%d %H:%M:%S')
        if int(self.monit_info["json"]) == 1 and self.monit_info["json_array"]:
           array=str(self.monit_info["json_array"])
           variable=str(self.monit_info["json_variable"])
           parameter=str(self.monit_info["parameter"])
           js=json.loads(html)
           if str(js[array][variable]) == parameter:
              self.patrol_right(self.monit_info,url,ip)                                                     # To determine whether the state is restored
           else:
              information=array+' '+variable+": "+str(js[array][variable])+" - Keyword:"+parameter
              self.patrol_wrong(self.monit_info,url,ip,information)
        elif int(self.monit_info["json"]) == 1 and self.monit_info["json_variable"]:                        # Analysis Json
           variable=str(self.monit_info["json_variable"])
           parameter=str(self.monit_info["parameter"])
           js=json.loads(html)
           if str(js[variable]) == parameter:
              self.patrol_right(self.monit_info,url,ip)
           else:
              information=variable+": "+str(js[variable])+" Keyword: "+parameter
              self.patrol_wrong(self.monit_info,url,ip,information)
        elif str(self.monit_info["parameter"]) in html:
            self.patrol_right(self.monit_info,url,ip)
        else:
            information="Keyword "+str(self.monit_info["parameter"])+" does not exist"
            self.patrol_wrong(self.monit_info,url,ip,information)
            name = self.monit_info["name"]+'_'+ip
            header = self.monit_info["header"]
            self.log(name,url,information,1,header)
           
    def patrol_right(self,monit_info,url,ip):                                                               # Analysis of normal
        name = ''
        name = self.monit_info["name"]+'_'+ip
        taskinfo = DAL.get_web_status(name)
        if taskinfo:
            if int(taskinfo[0]["status"]) > int(taskinfo[0]["level"]):
                alarm_status = '1'
                information = 'Recovery'
                frequency = '0'
                alarm_info = DAL.get_web_alarm_status(name)
                if alarm_info:
                    DAL.update_web_alarm_status(name,information,alarm_status,frequency)
                else:
                    DAL.insert_web_alarm_status(name,url,alarm_status,information,frequency,self.monit_info["header"],self.monit_info["name"])
                DAL.delete_web_status(name)
            else:
                DAL.delete_web_status(name)


    def patrol_wrong(self,monit_info,url,ip,information):                                                    # Error Analysis
        date = datetime.datetime.now()
        name = ''
        name = self.monit_info["name"]+'_'+ip
        taskinfo = DAL.get_web_status(name)
        if taskinfo:
            status = int(taskinfo[0]["status"])+1
            DAL.update_web_status(name,status)
            taskinfo = DAL.get_web_status(name)
            if int(taskinfo[0]["status"]) > int(taskinfo[0]["level"]):
                alarm_status = '0'
                alarm_info = DAL.get_web_alarm_status(name)
                if alarm_info == None:
                    frequency = '1'
                    DAL.insert_web_alarm_status(name,url,alarm_status,taskinfo[0]["information"],frequency,self.monit_info["header"],self.monit_info["name"])
                else:
                    frequency = taskinfo[0]["status"]
                    if "'" in taskinfo[0]["information"]:
                        information=taskinfo[0]["information"].replace("'","")
                    else:
                        information=taskinfo[0]["information"]
                    DAL.update_web_alarm_status(name,information,alarm_status,frequency)


        else:
            level = self.monit_info["level"]
            status = '1'
            DAL.insert_web_status(name,url,ip,level,status,date,information,self.monit_info["name"])
            taskinfo = DAL.get_web_status(name)
            if int(taskinfo[0]["status"]) > int(taskinfo[0]["level"]):
                alarm_status = '0'
                frequency = '1'
                DAL.insert_web_alarm_status(name,url,alarm_status,taskinfo[0]["information"],frequency,self.monit_info["header"],self.monit_info["name"])

    def log(self,name,url,error,times,header):
        date = datetime.datetime.now()
        date=date.strftime('%Y-%m-%d %H:%M:%S')
        DAL.insert_web_logs(date,name,url,error,times,header)
    
    def stop(self):
        self.stopped = True

# Custom Script entry
class WEBMONIT:
    @staticmethod
    def start(): 
        global g_queueURL
        taskUrl = DAL.get_monit_data()                                              # Get monitoring information
        detectname="Handcraft"                                                      # Check the settings name
        threadnum=20                                                                # The default number of threads
        if taskUrl:                                                                 # To determine whether the monitoring data is empty
            DETECT=detect(detectname,taskUrl,threadnum)                             # Transfer to detect class start detecting
