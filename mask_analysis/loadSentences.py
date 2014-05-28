# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 10:00:37 2014

@author: zqh
"""

import mysql.connector

import numpy as np

def sqlExec(sql_Query):
    config={'host':'192.168.3.197',
            'user':'fxk',  
            'password':'123456',  
            'port':3306 ,
            'database':'airpollution',  
            'charset':'utf8'
            }  
    try:  
        cnn=mysql.connector.connect(**config)  
    except mysql.connector.Error as e:  
        print('connect fails!{}'.format(e))
    
    cursor=cnn.cursor()  
    try:            
        cursor.execute(sql_Query)
        fetched=cursor.fetchall() 
    except mysql.connector.Error as e:  
        print('query error!{}'.format(e))  
    finally:  
        cursor.close()  
        cnn.close()  
    return fetched
SQL_Query_text='''
select text from
(
SELECT * from kz_bj_2013_nodup  where
   text not like '%%%%室内%%%%'
     and text not like '%%%%甲醛%%%%'
     and text not like '%%%%【%%%%】%%%%'
     and text not like '%%%#%%%#%%%'
     and text not like '%%%南京%%%'
     and text not like '%%%%武汉%%%%%'
     and text not like '%%%%江苏%%%%%'
     and loc like '%%%%北京%%%%'
      and source not like '%%%%时光机%%%'
  #########filter   
     and source not like '%%%全国空气污染指数%%%%'
     and isRetweet = 0
     
      and source not like  '%%%墨迹天气%%%'  
      and source not like '%%%%天气通%%%%'
     
     ###23333
 and text not like '%%%http%%%%'
   ) as temp 
   
'''

KZ_text =  sqlExec(SQL_Query_text)

import random
KZ_text_sample = random.sample(KZ_text,2000)

KZ_text_sample = np.array(KZ_text_sample)

KZ_text = np.array(KZ_text)




#output=open('kouzhao.txt', 'wb')

#for item in KZ_text:         
#    output.write(item[0])












