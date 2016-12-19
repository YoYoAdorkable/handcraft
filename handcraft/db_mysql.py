# -*- coding:utf-8 -*-

# The main program: db_mysql.py
# Date: 2015-12-24 
# Mail: yuhailong880106@gmail.com
# Features: Database Package


import sys
import MySQLdb
from MySQLdb.cursors import DictCursor

class MYSQL:
    def __init__(self, **kwargs):
        self.base = kwargs.get('base')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.host = kwargs.get('host')

        self.db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.password,
                             db=self.base,
                             charset='utf8',
                             cursorclass=DictCursor)

        self.cursor = self.db.cursor()

    def execute(self, sql,param = None):
        self.cursor.execute(sql,param)
        return self.cursor.fetchall()

    def update(self, sql,param = None):
        self.cursor.execute(sql,param)
        self.db.commit()
        return self.cursor.fetchall()

    def select(self, table, *args, **kwargs):
        """

        """
        # what values need select
        selected = '*' if not args else ', '.join([arg for arg in args])

        sql = 'SELECT {selected} FROM {table}'.format(table=table, selected=selected)

        if kwargs:
        # format kwargs into sql format
            where = ['{key}="{value}"'.format(key=key, value=value) for key, value in kwargs.iteritems()]
            where = ' WHERE' +' AND '.join(where)
            sql += where

        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def insert(self, table, **kwargs):
        """

        """
        field_names = ', '.join(kwargs.keys())

        values = '"'+'", "'.join(kwargs.values()) + '"'

        sql = 'INSERT INTO {table}({field_names}) VALUES({values})'.format(table=table,
                                                                    field_names=field_names,
                                                                    values=values)
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()


    def delete(self, table, **kwargs):
        """
        """
        # format kwargs into sql format
        where = ['{key}="{value}"'.format(key=key, value=value) for key, value in kwargs.iteritems()]
        sql = 'DELETE FROM {table} WHERE {where}'.format(table=table, where=' AND '.join(where))
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.db.close()


    # db = DBClass(base='test', user='root', password='qazedc', host='localhost')
    #db.delete('users', fname='Ivan')
    #db.insert('users', fname='Ivan', lname='Ivanov', nickname='ivanko')
    # print db.select('users')



