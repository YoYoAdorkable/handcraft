# -*- coding:utf-8 -*-

# The main program: db_DAL.py
# Date: 2015-12-24 
# Mail: yuhailong880106@gmail.com
# Features: Mysql statement


from db_config import *
from db_mysql import *
import time
import os,sys

class DAL():

    @staticmethod
    def getDB():
        return MYSQL( host= mysql_conn['host'],base=mysql_conn['db'], user= mysql_conn['user'], password= mysql_conn['passwd'],)

#####################################################################################################################################

# Extract data

    # Get ip address: hmonit_monit
    @staticmethod
    def get_ip_adderss():
        db = DAL.getDB()
        sql = "select ip from hmonit_monit where rule = 1"
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None
#-----------------------------------------------------------------------------------------------------------------------------------

    # Get ip address status: hmonit_ip_status
    @staticmethod
    def get_ip_results(ip):
        db = DAL.getDB()
        sql = "select status from hmonit_ip_status where ip = '%s'" %ip
        task = db.execute(sql)
        db.close

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------

    # Get ip alarm status: hmonit_ip_alarm_status
    @staticmethod
    def get_ip_alarm_results():
        db = DAL.getDB()
        sql = "select ip,status from hmonit_ip_alarm_status"
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------
    
    # Get Contact alarm: huser_user
    @staticmethod
    def get_user_contact(gid):
        if int(gid) == 0:
            db = DAL.getDB()
            sql = "select hus.email,hus.phone from huser_user hus,(select hug.user_id as ui from  huser_user_group hug,(select id FROM huser_usergroup where name = 'ops') hu where hug.usergroup_id=hu.id) hh where hus.id=hh.ui and hus.is_active = '1';"
            task = db.execute(sql)
            db.close()

            if task:
                return task
            else:
                return None
        else:
            db = DAL.getDB()
            sql = "select hus.email,hus.phone from huser_user hus,(select hug.user_id as ui from  huser_user_group hug,(select id FROM huser_usergroup where name = 'ops') hu,(select usergroup_id FROM hmonit_monit_contact where monit_id = %d) hm where hug.usergroup_id=hu.id or hug.usergroup_id=hm.usergroup_id) hh where hus.id=hh.ui and hus.is_active = '1';" %int(gid)
            task = db.execute(sql)
            db.close()

            if task:
                return task
            else:
                return None

#-----------------------------------------------------------------------------------------------------------------------------------

    # Get header: hmonit_monit
    @staticmethod
    def get_header_info(ip):
        db = DAL.getDB()
        sql = "select header from hmonit_monit where ip like '%%%s%%'" %str(ip)
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------

    # Get url: hmonit_monit
    @staticmethod
    def get_url_info(ip):
        db = DAL.getDB()
        sql = "select url from hmonit_monit where ip like '%%%s%%'" %str(ip)
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------

    # Get name: hmonit_monit
    @staticmethod
    def get_name_info(ip):
        db = DAL.getDB()
        sql = "select name from hmonit_monit where ip like '%%%s%%'" %str(ip)
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None


#-----------------------------------------------------------------------------------------------------------------------------------

    # Obtain monitoring data: hmonit_monit
    @staticmethod
    def get_monit_data():
        db = DAL.getDB()
        sql = "select * from hmonit_monit"
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------
    
    # Get webmonit status: hmonit_web_status
    @staticmethod
    def get_web_status(name):
        db = DAL.getDB()
        sql = "select * from hmonit_web_status where name = '%s'" %str(name)
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------
    
    # Get alarm status: hmonit_web_alarm_status
    @staticmethod
    def get_web_alarm_status(name):
        db = DAL.getDB()
        sql = "select * from hmonit_web_alarm_status where name = '%s'" %str(name)
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------

    # Get web alarm status: hmonit_web_alarm_status
    @staticmethod
    def get_alarm_web_status():
        db = DAL.getDB()
        sql = "select * from hmonit_web_alarm_status"
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------
    
    # Get monit id : hmonit_monit
    @staticmethod
    def get_monit_id(name):
        db = DAL.getDB()
        sql = "select id from hmonit_monit where name = '%s';" %str(name)
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------

    # Get monit web alarm frequency: hmonit_web_alarm_status
    @staticmethod
    def get_web_alarm_frequency(name):
        db = DAL.getDB()
        sql = "select frequency from hmonit_web_alarm_status where name = '%s';" %str(name)
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------

    #Get monit level: hmonit_monit
    @staticmethod
    def get_monit_level(name):
        db = DAL.getDB()
        sql = "select level from hmonit_monit where name = '%s';" %str(name)
        task = db.execute(sql)
        db.close()

        if task:
            return task
        else:
            return None

#-----------------------------------------------------------------------------------------------------------------------------------

#####################################################################################################################################

# Storing data

    # Insert ip status: hmonit_ip_status
    @staticmethod
    def insert_ip_results(ip,status,name):
        ip = str(ip)
        status = str(status)
        name = str(name)
        db = DAL.getDB()
        task = db.insert("hmonit_ip_status",name = name,status = status,ip = ip)
        db.close()

#-----------------------------------------------------------------------------------------------------------------------------------

    # Insert ip alarm status: hmonit_ip_alarm_status
    @staticmethod
    def insert_ip_alarm_results(ip,status):
        ip = str(ip)
        status = str(status)
        db = DAL.getDB()
        task = db.insert("hmonit_ip_alarm_status",status = status,ip = ip)
        db.close()

#-----------------------------------------------------------------------------------------------------------------------------------

    # Insert web status: hmonit_web_status
    @staticmethod
    def insert_web_status(name,url,ip,level,status,date,information,name1):
        name = str(name)
        url = str(url)
        ip = str(ip)
        level = str(level)
        status = str(status)
        date = str(date)
        name1 = str(name1)
        db = DAL.getDB()
        task = db.insert("hmonit_web_status",name = name,url = url,ip = ip,level = level,status = status,date = date,information = information,name1 = name1)
        db.close()

#-----------------------------------------------------------------------------------------------------------------------------------

    # Insert web alarm status: hmonit_web_alarm_status
    @staticmethod
    def insert_web_alarm_status(name,url,status,information,frequency,header,name1):
        name = str(name)
        url = str(url)
        status = str(status)
        information = str(information)
        header = str(header)
        name1 = str(name1)
        db = DAL.getDB()
        task = db.insert("hmonit_web_alarm_status",name = name,url = url,status = status,information = information,frequency = frequency,header = header,name1 = name1)
        db.close()

#-----------------------------------------------------------------------------------------------------------------------------------

    # Inesert web logs: hlog_web_logs
    @staticmethod
    def insert_web_logs(date,name,url,error,times,header):
        date = str(date)
        name = str(name)
        url = str(url)
        error = str(error)
        times = str(times)
        header = str(header)
        db = DAL.getDB()
        task = db.insert("hlog_web_logs",date = date,name = name,url = url,error = error,times = times,header = header)
        db.close()
        




#####################################################################################################################################

# Update data

    # Update ip address status: hmonit_ip_status
    @staticmethod
    def update_ip_results(ip,status,name):
        db = DAL.getDB()
        sql = "update hmonit_ip_status SET status = '%s',name = '%s' WHERE ip = '%s';" %(str(status),str(name),ip)
        task = db.update(sql)
        db.close()

#-----------------------------------------------------------------------------------------------------------------------------------

    # Update web status: hmonit_web_status
    @staticmethod
    def update_web_status(name,status):
        db = DAL.getDB()
        sql = "update hmonit_web_status set status = '%s' where name = '%s';" %(str(status),str(name))
        task = db.update(sql)
        db.close()

#-----------------------------------------------------------------------------------------------------------------------------------

    # Update web alarm status: hmonit_web_alarm_status
    @staticmethod
    def update_web_alarm_status(name,information,status,frequency):
        db = DAL.getDB()
        sql = "update hmonit_web_alarm_status set information = '%s',frequency = '%s',status = '%s' where name = '%s';" %(str(information),str(frequency),str(status),str(name))
        task = db.update(sql)
        db.close()

#-----------------------------------------------------------------------------------------------------------------------------------

#####################################################################################################################################

# Deleting Data

    # Delete web status: hmonit_web_status
    @staticmethod
    def delete_web_status(name):
        db = DAL.getDB()
        task = db.delete("hmonit_web_status",name = name)
        db.close()

#-----------------------------------------------------------------------------------------------------------------------------------

    # Delete web alarm status: hmonit_web_alarm_status
    @staticmethod
    def delete_web_alarm_status(status):
        db = DAL.getDB()
        task = db.delete("hmonit_web_alarm_status",status = status)
        db.close

#-----------------------------------------------------------------------------------------------------------------------------------

    # Delete ip alarm status: hmonit_ip_alarm_status
    @staticmethod
    def delete_ip_alarm_status(status):
        db = DAL.getDB()
        task = db.delete("hmonit_ip_alarm_status",status = status)
        db.close


#####################################################################################################################################

# Clear Data
 
    # clear table: hmonit_ip_alarm_status
    @staticmethod
    def clear_ip_alarm_results():
        db = DAL.getDB()
        sql = "truncate hmonit_ip_alarm_status"
        task = db.execute(sql)
        db.close()

#####################################################################################################################################
