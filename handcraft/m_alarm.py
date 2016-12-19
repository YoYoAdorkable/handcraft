
#coding:utf-8

# Alarm program: m_alarm.py
# Date: 2015-12-24
# Mail: yuhailong880106@gmail.com
# Features: Alarm Email and SMS

import time
import os,sys
import socket
import urllib
import smtplib
from email.mime.text import MIMEText
from db_DAL import *

reload(sys)
sys.setdefaultencoding( "utf-8" )


class ALARM():
   
#-----------------------------------------------------------------------------------------------------------------------------------
    # Get ip alarm status
    @staticmethod
    def ip_alarm():
        alarm_status = DAL.get_ip_alarm_results()
        if alarm_status:
            for num in range(len(alarm_status)):
                if int(alarm_status[num]["status"]) == 1:
                    ALARM.ip_recovery_alarm(alarm_status[num]["ip"],alarm_status[num]["status"])
                else:
                    ALARM.ip_down_alarm(alarm_status[num]["ip"],alarm_status[num]["status"])

    # ip recovery alarm
    @staticmethod
    def ip_recovery_alarm(ip,status):
        hostname = socket.getfqdn(socket.gethostname(  ))
        hostaddr = socket.gethostbyname(hostname)
        contact = DAL.get_user_contact(0)
        content="SMS: Network Monitoring - "+str(ip)+" - {Network Recovery} - Alarm host: "+str(hostaddr)
        ALARM.send_sms(contact,content)
        ALARM.send_ip_mail(ip,contact,str(content))
        DAL.delete_ip_alarm_status('1')

    # ip down alarm
    @staticmethod 
    def ip_down_alarm(ip,status):
        hostname = socket.getfqdn(socket.gethostname(  ))
        hostaddr = socket.gethostbyname(hostname)
        contact = DAL.get_user_contact(0)
        content="SMS: Network Monitoring - "+str(ip)+" - {Network Error} - Alarm host: "+str(hostaddr)
        ALARM.send_sms(contact,content)
        ALARM.send_ip_mail(ip,contact,str(content))

#-----------------------------------------------------------------------------------------------------------------------------------

    # Get web alarm status: hmonit_web_alarm_status
    @staticmethod 
    def web_alarm():
        alarm_info = DAL.get_alarm_web_status()
        if alarm_info:
            for num in range(len(alarm_info)):
                if int(alarm_info[num]["status"]) == 1:
                    ALARM.web_recovery_alarm(alarm_info[num]["name"],alarm_info[num]["information"])
                else:
                    ALARM.web_down_alarm(alarm_info[num]["name"],alarm_info[num]['information'])

    # web recovery alarm
    @staticmethod 
    def web_recovery_alarm(name,information):
        web_name = ALARM.web_name_split(name)
        web_id = DAL.get_monit_id(web_name)
        if web_id:
            hostname = socket.getfqdn(socket.gethostname(  ))
            hostaddr = socket.gethostbyname(hostname)
            contact = DAL.get_user_contact(web_id[0]["id"])
            content="SMS: Web Monitoring -"+str(name)+" - {Web Recovery} - Alarm host: "+str(hostaddr)
            ALARM.send_sms(contact,content)
            ALARM.submit_web_mail(contact,str(content))
            DAL.delete_web_alarm_status('1')


    # web down alarm
    @staticmethod 
    def web_down_alarm(name,information):
        web_name = ALARM.web_name_split(name)
        web_id = DAL.get_monit_id(web_name)
        if web_id:
            hostname = socket.getfqdn(socket.gethostname(  ))
            hostaddr = socket.gethostbyname(hostname)
            contact = DAL.get_user_contact(web_id[0]["id"])
            if 'Read timed out' in information:
                information='Connection timeout'
            elif 'Connection refused' in information:
                information='Connection refused'
            elif '502' in information:
                information='502 Bad Gateway'
            elif '503' in information:
                information='503 Service Unavailable'
            elif '404' in information:
                information='404 Not Found'
            elif '500' in information:
                information='500 Internal Server Error'
            elif 'HTTPConnectionPool' in information:
                information = information.split('(')[1].split(')')[0]+' Connection refused'

            level = DAL.get_monit_level(web_name)
            if int(level[0]["level"]) == 0:
                content="SMS[H]: Web Monitoring -"+str(name)+" - {"+information+"} - Alarm host: "+str(hostaddr)
            elif int(level[0]["level"]) == 2:
                content="SMS[M]: Web Monitoring -"+str(name)+" - {"+information+"} - Alarm host: "+str(hostaddr)
            elif int(level[0]["level"]) == 4:
                content="SMS[L]: Web Monitoring -"+str(name)+" - {"+information+"} - Alarm host: "+str(hostaddr)
            else:
                content="SMS[VL]: Web Monitoring -"+str(name)+" - {"+information+"} - Alarm host: "+str(hostaddr)
            
            frequency = DAL.get_web_alarm_frequency(name)
            if int(frequency[0]["frequency"]) < 3 or (int(frequency[0]["frequency"]) > 30 and int(frequency[0]["frequency"]) < 33) or (int(frequency[0]["frequency"]) > 88 and int(frequency[0]["frequency"]) < 90):
                ALARM.send_sms(contact,content)
                ALARM.submit_web_mail(contact,str(content))
    
    # split name
    @staticmethod
    def web_name_split(name):
        name = name.split('_')
        name.pop()
        web_name = '_'.join(name)
        return web_name
#-----------------------------------------------------------------------------------------------------------------------------------

    # send sms
    @staticmethod
    def send_sms(contact,content):
        if '115.182' in content or '125.62.12.146' in content or '192.168.0.37' in content:
            contact = DAL.get_user_contact(0)
            for num in range(len(contact)):
                if contact[num]["phone"]:
                    print (time.strftime("%Y/%m/%d %H:%M:%S")),contact[num]["phone"]+'_send_sms'
                    sms="http://sms.in.kuyun.com/sms.do?mobile="+contact[num]["phone"]+"&content="+content
                    send = urllib.urlopen(str(sms))
        else:
            for num in range(len(contact)):
                if contact[num]["phone"]:
                    print (time.strftime("%Y/%m/%d %H:%M:%S")),contact[num]["phone"]+'_send_sms'
                    sms="http://sms.in.kuyun.com/sms.do?mobile="+contact[num]["phone"]+"&content="+content
                    send = urllib.urlopen(str(sms))

#-----------------------------------------------------------------------------------------------------------------------------------

    # send ip mail
    @staticmethod
    def send_ip_mail(ip,contact,content):
        header = DAL.get_header_info(ip)
        headers = ''
        if header:
            for num in range(len(header)):
                if header[num]["header"] not in headers:
                    headers = headers+' '+header[num]["header"]
            content=content+" - Domain_Name:"+headers
            ALARM.submit_ip_mail(contact,content)


    # Submit ip e-mail
    @staticmethod
    def submit_ip_mail(contact,content):
        mailto_list=[]
        if '115.182' in content or '125.62.12.146' in content or '192.168.0.37' in content:
            contact = DAL.get_user_contact(0)
            for num in range(len(contact)):
                if contact[num]["email"]:
                    mailto_list.append(contact[num]["email"])

            if 'Error' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Down'
            elif 'Recovery' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Recovery'

            if ALARM.send_email(mailto_list,sub,content):
                print "邮件发送成功"
            else:
                print "邮件发送失败"
        else:
            for num in range(len(contact)):
                if contact[num]["email"]:
                    mailto_list.append(contact[num]["email"])

            if 'Error' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Down'
            elif 'Recovery' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Recovery'

            if ALARM.send_email(mailto_list,sub,content):
                print "邮件发送成功"
            else:
                print "邮件发送失败"

#-----------------------------------------------------------------------------------------------------------------------------------

    # Submit web e-mail
    @staticmethod
    def submit_web_mail(contact,content):
        mailto_list=[]
        if '115.182' in content or '125.62.12.146' in content or '192.168.0.37' in content:
            contact = DAL.get_user_contact(0)
            for num in range(len(contact)):
                if contact[num]["email"]:
                    mailto_list.append(contact[num]["email"])
            if 'Keyword' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Keyword does not match'
            elif 'Recovery' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Recovery'
            elif 'timeout' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Timeout'
            elif '404' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - 404'
            elif '500' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - 500'
            elif '502' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - 502'
            elif '503' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - 503'
            elif '504' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - 504'
            elif 'Connection refused' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Connection refused'
            else:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Error'
            
            if ALARM.send_email(mailto_list,str(sub),content):
                print "邮件发送成功"
            else:
                print "邮件发送失败"
        else:
            for num in range(len(contact)):
                if contact[num]["email"]:
                    mailto_list.append(contact[num]["email"])
            if 'Keyword' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Keyword does not match'
            elif 'Recovery' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Recovery'
            elif 'timeout' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Timeout'
            elif '404' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - 404'
            elif '500' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - 500'
            elif '502' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - 502'
            elif '503' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - 503'
            elif '504' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - 504'
            elif 'Connection refused' in content:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Connection refused'
            else:
                sub=content.split('-')[0]+' - '+content.split('-')[1]+' - Error'
        
            if ALARM.send_email(mailto_list,str(sub),content):
                print "邮件发送成功"
            else:
                print "邮件发送失败"

#-----------------------------------------------------------------------------------------------------------------------------------

    # send email
    @staticmethod
    def send_email(mailto_list,sub,content):
        mail_host="smtp.qq.com"
        mail_user="admin@kuyun.com"
        mail_pass="tenfen1234"
        mail_postfix="kuyun.com"

        '''
        mailto_list:发给谁
        sub:主题
        content:内容
        send_mail("1221@163.com","sub","content")
        '''
        me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
        msg = MIMEText(content)
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(mailto_list)
        try:
            s = smtplib.SMTP()
            s.connect(mail_host)
            s.login(mail_user,mail_pass)
            s.sendmail(me, mailto_list, msg.as_string())
            s.close()
            return True
        except Exception, e:
            print str(e)
            return False
        
