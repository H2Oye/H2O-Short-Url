# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import config
import pymysql
import re
import time

class DataBase:
    def __init__(self):
        self.prefix = config.DATABASE.get('prefix')
        self.connect = pymysql.connect(
            host=config.DATABASE.get('host'),
            port=int(config.DATABASE.get('port')),
            user=config.DATABASE.get('username'),
            passwd=config.DATABASE.get('password'),
            db=config.DATABASE.get('database_name'),
            ssl_ca=config.DATABASE.get('ssl').get('ca_path'),
            ssl_key=config.DATABASE.get('ssl').get('key_path'),
            ssl_cert=config.DATABASE.get('ssl').get('cert_path')
        )
        self.cursor = self.connect.cursor(pymysql.cursors.DictCursor)

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def existenceTable(self, name):
        sql = 'show tables'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = re.findall('(\'.*?\')', str(data))
        data = [re.sub("'", '', data_count) for data_count in data]
        return f'{self.prefix}{name}' in data

    def createCoreTable(self):
        sql = f'''
            CREATE TABLE `{self.prefix}core` (
                `key_` varchar(255) NOT NULL,
                `value_` varchar(255) DEFAULT NULL,
                PRIMARY KEY (`key_`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

        sql = f'''
            INSERT INTO `{self.prefix}core` (key_, value_)
            VALUES(
                "title", "氧化氢短网址"
            );
        '''
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'''
            INSERT INTO `{self.prefix}core` (key_, value_)
            VALUES(
                "keyword", "氧化氢短网址"
            );
        '''
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'''
            INSERT INTO `{self.prefix}core` (key_, value_)
            VALUES(
                "description", "一切是那么的简约高效."
            );
        '''
        self.cursor.execute(sql)
        self.connect.commit()

    def createDomainTable(self):
        sql = f'''
            CREATE TABLE `{self.prefix}domain` (
                `domain` varchar(255) NOT NULL,
                `protocol` varchar(255) DEFAULT NULL,
                PRIMARY KEY (`domain`) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

    def createUrlTable(self):
        sql = f'''
            CREATE TABLE `{self.prefix}url` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `type_` varchar(255) DEFAULT NULL,
                `domain` varchar(255) DEFAULT NULL,
                `long_url` varchar(255) DEFAULT NULL,
                `signature` varchar(255) DEFAULT NULL,
                `valid_day` int(11) DEFAULT NULL,
                `count` int(11) DEFAULT NULL,
                `timestmap` int(11) DEFAULT NULL,
                PRIMARY KEY (`id`) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

    def insert(self, type_, domain, longUrl, validDay):
        sql = f'''
            INSERT INTO {self.prefix}url (type_, domain, long_url, valid_day, count, timestmap)
            VALUES(
                "{type_}",
                "{domain}",
                "{longUrl}",
                {validDay},
                0,
                {int(time.time())}
            );
        '''
        self.cursor.execute(sql)
        id_ = self.connect.insert_id()
        self.connect.commit()
        return id_
    
    def update(self, id_, signature):
        sql = f'''
            UPDATE {self.prefix}url 
            SET signature = "{signature}" 
            WHERE
                id = {id_} 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        self.connect.commit()
    
    def delete(self, id_):
        sql = f'''
            DELETE 
            FROM
                {self.prefix}url 
            WHERE
                id = "{id_}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        self.connect.commit()

    def addCount(self, domain, signature):
        sql = f'''
            UPDATE {self.prefix}url 
            SET count = count + 1 
            WHERE
                domain = "{domain}" 
                AND signature = "{signature}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        self.connect.commit()
    
    def queryWebsiteInfo(self):
        sql = f'''
            SELECT
                * 
            FROM
                {self.prefix}core 
            WHERE
                key_ = "title" 
                OR key_ = "keyword" 
                OR key_ = "description" 
            LIMIT 3;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data_ = {}
        for datum in data:
            data_[datum.get('key_')] = datum.get('value_')
        return data_

    def queryDomain(self):
        sql = f'''
            SELECT
                * 
            FROM
                {self.prefix}domain;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data_ = {}
        for datum in data:
            data_[datum.get('domain')] = datum.get('protocol')
        return data_

    def queryUrlByLongUrl(self, domain, longUrl):
        sql = f'''
            SELECT
                * 
            FROM
                {self.prefix}url 
            WHERE
                domain = "{domain}" 
                AND long_url = "{longUrl}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        return False

    def queryUrlBySignature(self, domain, signature):
        sql = f'''
            SELECT
                * 
            FROM
                {self.prefix}url 
            WHERE
                domain = "{domain}" 
                AND signature = "{signature}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        return False