# -*- coding: utf-8 -*-
"""
Created on Thu May 15 10:13:28 2014

@author: zqh
"""

import mysql.connector
import datetime


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


def smoothYearDataTime_weioNum(weiboNum):

    startTime=datetime.date(2013,1,1)
    endTime=datetime.date(2013,12,31)
    aDay=datetime.timedelta(days=1)

    year2013=set()

    returnData = []
    while startTime <= endTime:
        for item in weiboNum:
            if item[0] ==  startTime:
            
                returnData +=[item]
                
                test= item[0]
#                print test
                break
        if test != startTime:
            
            returnData += [(startTime,-1) ]
            
            print '^^'
        year2013.add(startTime) 
        
        startTime+=aDay
        
    weibo_date_set=set()
    
    for item in weiboNum:
        weibo_date_set.add(item[0])                
    day_that_we_donot_have=year2013-weibo_date_set
    
   
    return returnData,day_that_we_donot_have
    
def loadWM_num():    
    sqL='''
    select createAt,count(createAt) as cnt from
    (
    SELECT date(createAt) as createAt from wm_bj_2013_nodup  where
       text not like '%%%%室内%%%%'
         and text not like '%%%%甲醛%%%%'
         and text not like '%%%%【%%%%】%%%%'
         and text not like '%%%#%%%#%%%'
         and text not like '%%%南京%%%'
         and text not like '%%%%武汉%%%%%'
         and text not like '%%%%江苏%%%%%'
           and text not like '%%%%江苏%%%%%'
           
           
          and text not like '%%%%口罩%%%'
          and text not like '%%%空气污染%%%%'
      #########filter   
         and source not like '%%%全国空气污染指数%%%%'
         and isRetweet = 0
         
          and source not like  '%%%墨迹天气%%%'  
         and source not like '%%%%天气通%%%%'
         and source not like '%%%%皮皮时光机%%%%'
         ###23333
    # and  text not like '%%%http%%%%'
    ) as temp
    group by createAt
    
    
    '''
    KQWR_data=sqlExec(sqL)
    return smoothYearDataTime_weioNum(KQWR_data)
    
WM_num,WM_day_loss = loadWM_num()








