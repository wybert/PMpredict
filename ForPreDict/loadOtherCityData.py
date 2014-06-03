# -*- coding: utf-8 -*-
"""
Created on Wed May 21 15:18:38 2014

@author: zqh
"""
import csv
import string
import datetime
import numpy as np
import mysql.connector
##load weather data

def loadIndex(filename):
    Index=csv.reader(file(filename,'r'))
    returnIndex=[]
    for row in Index:
        index=string.atoi(row[3])
        cfig = row[2].split('-')
        cfig=[string.atoi(i) for i in cfig]
        date=datetime.date(*cfig)    
        returnIndex.append([date]+[index])
    returnIndex=np.array(returnIndex)
    sortedNU = np.argsort(returnIndex[:,0])
    returnIndex = returnIndex[sortedNU,:]
    return returnIndex



# load weather index  
def loadWeatherIndex(filename):
    Index=csv.reader(file(filename,'r'))
    returnIndex=[]
    for row in Index:
        returnIndex.append(row)    
    return returnIndex


def process_loadedFile(filename):

    loadedfile=loadWeatherIndex(filename)
    
    fengxiangSet=set()
    fengliSet=set()
    for item in loadedfile:  
#        print item[4]
        fengxiang=item[4].split("~")
        for feng in fengxiang:
#            print feng
            fengxiangSet.add(feng)     
        fengli=item[5].split('~')
        for feng in fengli:
            fengliSet.add(feng)
            
    print '----------weather-------------------'    
    print 'fengxiangSet:',len(fengxiangSet)
    for i in fengxiangSet:
        print i
    print 'fengliSet:',len(fengliSet)
    for i in fengliSet:
        print i

    processed_file=[]

    for item in loadedfile: 

        temp=item[0].split('-')
        temp=[string.atoi(i) for i in temp]
        date=datetime.date(*temp)

       
       
        temperature_high=string.atoi(item[1].strip(u'℃'))
       
        temperature_low=string.atoi(item[2].strip(u'℃'))
       
       
        tianqi=[u'晴',u'云',u'阴',u'雨',u'雾',u'霾',u'雪',u'沙',u'雷']
        weather=[1 for i in tianqi]
        for i in range(len(tianqi)):
            if item[3].find(tianqi[i]) == -1:
                weather[i]=0                   
     
    
        fengxiang=[1 for i in fengxiangSet]
        fengxiangSet=list(fengxiangSet)
        for i in range(len(fengxiangSet)):
            if item[4].find(fengxiangSet[i]) == -1:
                fengxiang[i]=0       
        fengli=[1 for i in fengliSet]
        fengliSet=list(fengliSet)
       
        for i in range(len(fengliSet)):
            if item[5].find(fengliSet[i]) == -1:
                fengli[i]=0
                      
        processed_file+=[ [date]+[temperature_high]+[temperature_low]+[weather]+[fengxiang]+[fengli] ]
    return processed_file

# and weibo number 

#KQWR in xiamen

def loadYYFILE(filename):
    XMKQWR=csv.reader(file(filename,'r'))
    XMKQWR=list(XMKQWR)
    startTime=datetime.date(2014,1,1)
    endTime=datetime.date(2014,4,30)
    aDay=datetime.timedelta(days=1)
    daylist=[]
    
    while startTime <= endTime:

        good,bad,other=0,0,0

#        print 'start:',startTime
        
        for item in XMKQWR:
            temp=item[0].split('-')
            temp=[string.atoi(i) for i in temp]
            date=datetime.date(*temp)
 
            if date == startTime:
#                print "^^"
                if item[2] == '1':
                    bad+=1
                elif item[2] == '-1':
                    good+=1
                elif item[2] == '0':
                    other +=1
                else:
                    print 'wrong'

        daylist += [[startTime]+[good]+[bad]+[other]]

#        print 'ended:',startTime
        startTime += aDay
  
#        print startTime
    return daylist


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

def smoothSHDataTime(data):

    startTime=datetime.date(2014,1,1)
    endTime=datetime.date(2014,1,31)
    aDay=datetime.timedelta(days=1)

    year2014=set()

    returnData = []
    while startTime <= endTime:
        for item in data:
            if item[0] ==  startTime:
#                print item[0]
            
                returnData +=[item]
                
                test= item[0]
#                print test
                break
        try:
            if test != startTime:
                
                returnData += [(startTime,0) ]
                
#                print '^^'
        except:
            returnData += [(startTime,0) ]
        year2014.add(startTime) 
        
        startTime+=aDay
        
    weibo_date_set=set()
    
    for item in data:
        weibo_date_set.add(item[0])                
    day_that_we_donot_have=year2014-weibo_date_set
    
   
    return returnData,day_that_we_donot_have    
def smoothYearDataTime_weioNum(weiboNum):

    startTime=datetime.date(2014,1,1)
    endTime=datetime.date(2014,4,30)
    aDay=datetime.timedelta(days=1)

    year2014=set()

    returnData = []
    while startTime <= endTime:
        for item in weiboNum:
            if item[0] ==  startTime:
#                print item[0]
            
                returnData +=[item]
                
                test= item[0]
#                print test
                break
        try:
            if test != startTime:
                
                returnData += [(startTime,0) ]
                
#                print '^^'
        except:
            returnData += [(startTime,0) ]
        year2014.add(startTime) 
        
        startTime+=aDay
        
    weibo_date_set=set()
    
    for item in weiboNum:
        weibo_date_set.add(item[0])                
    day_that_we_donot_have=year2014-weibo_date_set
    
   
    return returnData,day_that_we_donot_have
#KZ

def loadXM_KZ_NUM():
    
    SQL_Query='''
 select createAt,count(createAt) as daycot from
    (
    
        SELECT date(createAt) as createAt from kqwr_kz_xm_2014_nodup  where
        
           keyword like  "%%%口罩%%%"
     and text not like '%%%%室内%%%%'
         and text not like '%%%%甲醛%%%%'
         and text not like '%%%%【%%%%】%%%%'
         and text not like '%%%#%%%#%%%'
         and text like '%%%%空气%%%%'
    
         and loc  like '%%%%厦门%%%%'
          and source not like '%%%%时光机%%%'
      #########filter   
      
         and isRetweet = 0
     
          and text not like '%%%%url%%%%'
         ###23333
     and text not  like '%%%http%%%%'
             
             
     
       ) as temp 
     
    group by  createAt'''

    
    XMKZNUM = sqlExec(SQL_Query)
#    print XMKZNUM
    
    return smoothYearDataTime_weioNum(XMKZNUM)
def loadSH_KZ_NUM():
    SQL_Query='''select createAt,count(createAt) as daycot from
    (
    
        SELECT date(createAt) as createAt from kqwr_kz_sh_2014_nodup  where
        
           keyword like  "%%%口罩%%%"
     and text not like '%%%%室内%%%%'
         and text not like '%%%%甲醛%%%%'
         and text not like '%%%%【%%%%】%%%%'
         and text not like '%%%#%%%#%%%'
         and text like '%%%%空气%%%%'
    
         and loc  like '%%%%上海%%%%'
          and source not like '%%%%时光机%%%'
      #########filter   
      
         and isRetweet = 0
     
          and text not like '%%%%url%%%%'
         ###23333
     and text not  like '%%%http%%%%'
             
             
     
       ) as temp 
     
    group by  createAt    
    '''
    SHKZNUM=sqlExec(SQL_Query)
    return smoothSHDataTime(SHKZNUM)
    

def normlizeWeiBo_num(weibo_num,populatiom):

    return weibo_num/populatiom
def process_XM_wether_data2(XM_Weather):

    for item in XM_Weather:
		item[4] = item[4][1]

    try:
        for item in XM_Weather:

            for i in range(len(item[5])):
                if item[5][0]:
                    item[5][0] = 3
                if item[5][1]:
                    item[5][1] = 5
                if item[5][2]:
                    item[5][2] = 4
               
            item[5] = np.max(item[5])
#            wind_power += [item[5]]
    except:
        pass

    weather_Feture=[]
    for item in XM_Weather:
#        print item[5]
        weather_Feture+=[ [item[0]]+[item[1]]+[item[2]] +[item[1]-item[2]]+item[3]+[item[4]]+[item[5]]   ]
    return weather_Feture
    
def process_SH_weather_data2(SH_Weather):

    for item in SH_Weather:
        item[4] = item[4][3]

    try:
        for item in SH_Weather:

            for i in range(len(item[5])):
                if item[5][0]:
                    item[5][0] = 3
                if item[5][1]:
                    item[5][1] = 5
                if item[5][2]:
                    item[5][2] = 4
               
            item[5] = np.max(item[5])
#            wind_power += [item[5]]
    except:
        pass

    weather_Feture=[]
    for item in SH_Weather:
#        print item[5]
        weather_Feture+=[ [item[0]]+[item[1]]+[item[2]] +[item[1]-item[2]]+item[3]+[item[4]]+[item[5]]   ]
    return weather_Feture	     

# uint wan
#
#beijing_pop=1297.46
#shanghai_pop=1426.93
#
#



XM_KZ_NUM,day_that_we_donot_have = loadXM_KZ_NUM()
XM_Weather = process_loadedFile('xiamenweather.csv')
XM_Weather = process_XM_wether_data2(XM_Weather)

XM_Index = loadIndex('xiamen.csv')
XM_Index,Index_loss = smoothYearDataTime_weioNum(XM_Index)
XM_Index = np.array(XM_Index)



#print np.max(XM_Index,axis=0)
#for item in XM_Index:
#    print item[0]


XMKQWR_yuyiResult = loadYYFILE('XMKQWR_yuyiResult.csv')



#---------------------------------------------------------


SH_KZ_NUM,day_that_we_donot_have = loadSH_KZ_NUM()

SH_Weather = process_loadedFile('shanghaiweather.csv')
SH_Weather = process_SH_weather_data2(SH_Weather)


SH_Weather,SH_Weather_dayloss = smoothSHDataTime(SH_Weather)
SH_Weather = np.array(SH_Weather)

SHKQWR_yuyiResult = loadYYFILE('SHKQWR_yuyiResult.csv')
SHKQWR_yuyiResult,SHKQWR_yuyiResult_dayloss=smoothSHDataTime(SHKQWR_yuyiResult)
SHKQWR_yuyiResult =np.array(SHKQWR_yuyiResult)

SHKZ_yuyiResult = loadYYFILE('SHKZ_sql_pre_data.csv')
SHKZ_yuyiResult,SHKZ_yuyiResult_dayloss=smoothSHDataTime(SHKZ_yuyiResult)
SHKZ_yuyiResult =np.array(SHKZ_yuyiResult)



SH_Idex = loadIndex('shanghai.csv')

SH_Idex,sh_idex_loss =smoothSHDataTime(SH_Idex)
SH_Idex = np.array(SH_Idex)


# ------------------------------------------------------
predict_dayloss=set()



