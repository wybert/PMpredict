# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 15:43:09 2014

@author: zqh
"""

import xlrd
import  datetime
import numpy as np
import string
import mysql.connector
import csv

####################################load index##########################################
# read xls file 

def loadOneFile_ofIndex(fname):
    bk=xlrd.open_workbook(fname)
    try:
        sh = bk.sheet_by_name("Sheet1")
    except:
        print "no sheet in %s named Sheet1" % fname
        
    nrows = sh.nrows
#    ncols = sh.ncols
    
#    print "nrows %d, ncols %d" % (nrows,ncols)
      
    row_list = []
    for i in range(1,nrows):
        row_data = sh.row_values(i)
        date_value = xlrd.xldate_as_tuple(sh.cell(i,1).value,bk.datemode) 
        row_data[1]= datetime.date(*date_value[:3])
#        print row_data[1]
        row_list.append(row_data)
    return row_list
    

#fname1="data/average_bj_7-12.xls"
#test=loadOneFile_ofIndex(fname1)


def load_File_ofIndex():
    fname1="data/average_bj_1-6.xls"
    fname2="data/average_bj_7-12.xls"
    loadedFileofIndex=loadOneFile_ofIndex(fname1)+loadOneFile_ofIndex(fname2)
    loadedFileofIndex=np.array(loadedFileofIndex)
    return loadedFileofIndex[:,1:4]



def load_index_of_day_mean():
    loadedFileofIndex=load_File_ofIndex()
    Myindex=[]
    for item in loadedFileofIndex[:,0:2]:
        if item[1] == '(no data)':
            pass
        else:
            Myindex += [item]
    
    startTime=datetime.date(2013,1,1)
    endTime=datetime.date(2013,12,31)
    aDay=datetime.timedelta(days=1)
    
    dayStaticContainer=[]
    
    while startTime <= endTime:
        adayTemp=[]
        for item in Myindex:
            if item[0]==startTime:
                adayTemp+=[item[1]]
        dayStaticContainer+=[[startTime]+[adayTemp]]     
        startTime+=aDay
    print '----------index-----------------------'
    print 'this days we dont have:'    
    i=0    
    for item in dayStaticContainer:
        if len(item[1])!=0:
            dayStaticContainer[i][1]=np.mean(item[1])
        else:
            print dayStaticContainer[i][0]
            dayStaticContainer[i][1]='null'
        i+=1
    return dayStaticContainer
    

#####################################load index2##########################################
## read xls file 
#
def loadOneFile_ofIndex_ofGPS(fname):
    bk=xlrd.open_workbook(fname)
    try:
        sh = bk.sheet_by_name("id")
    except:
        print "no sheet in %s named Sheet1" % fname
        
    nrows = sh.nrows
 
    row_list = []
    for i in range(1,nrows):
        row_data = sh.row_values(i)
        date_value = xlrd.xldate_as_tuple(sh.cell(i,0).value,bk.datemode) 
        row_data[0]= datetime.date(*date_value[:3])
#        print row_data[1]
        row_list.append(row_data)
    return row_list
#    
#
#fname1='data/GPS/yearwhole/month_1.xls'
#test=loadOneFile_ofIndex(fname1)
#

def load_index2():
    fname1='data/GPS/yearwhole/month_'
    fname2='.xls'
    loadedFileofIndex=[]
    for i in range(1,13):
        fname=fname1+str(i)+fname2
        loadedFileofIndex += loadOneFile_ofIndex_ofGPS(fname)        
    loadedFileofIndex=np.array(loadedFileofIndex)
    temp=[]
    for item in loadedFileofIndex[:,[0,2,6]]:
        if item[2] == u"城市环境评价点":
            temp+=[[item[0]]+[item[1]  ] ]
    
    timeStart=datetime.date(2013,1,1)
    timeEnd=datetime.date(2013,12,31)
    aDay=datetime.timedelta(days=1)
    
    index2=[]
    while timeStart <= timeEnd:
        temp2=[]
        for item in temp:
            if item[0] == timeStart and item[1] != u'-':
                temp2 += [item[1]]
    #    print temp2
            
        index2 += [[timeStart] + [np.mean(temp2)]]
        timeStart+=aDay
    
    return index2


###################################load weather data###########################################




def loadOneFile(fname):
    bk=xlrd.open_workbook(fname)
    try:
        sh = bk.sheet_by_name("Sheet1")
    except:
        print "no sheet in %s named Sheet1" % fname    
    nrows = sh.nrows

    row_list = []
    for i in range(1,nrows):
        row_data = sh.row_values(i)
        row_list.append(row_data)
    return row_list
    
def loadWeatherFile():
    fname1="data/weather/13." 
    fname3=".xls"
    loadedfile=[]
    for i in range(1,13):
        fname=fname1+str(i)+fname3    
        loadedfile+=loadOneFile(fname)
    return loadedfile



def process_loadedFile():
    loadedfile=loadWeatherFile()
    fengxiangSet=set()
    fengliSet=set()
    for item in loadedfile:  
        fengxiang=item[4].split("~")
        for feng in fengxiang:
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
        temp=item[0][0:10].split('-')
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
###############################load weibo data#######################################
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
        try:
            if test != startTime:
                returnData += [(startTime,0) ]
                print '^^'
        except:
            returnData += [(startTime,0)]

        year2013.add(startTime) 
        
        startTime+=aDay
        
    weibo_date_set=set()
    
    for item in weiboNum:
        weibo_date_set.add(item[0])                
    day_that_we_donot_have=year2013-weibo_date_set
    
   
    return returnData,day_that_we_donot_have



def load_weibo_num_from_database():
    sql_Query1='''
select createAt,count(createAt) as cont  from
(
SELECT date(createAt) as createAt  from status_bj_2013  where
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
 
 group by createAt





'''
    weibo_number_byDay=sqlExec(sql_Query1)
    
    
    return smoothYearDataTime_weioNum(weibo_number_byDay)

#  load weibo num consider time-------------------------------------------

def loadCreateAt():
    sql_Query1='''
SELECT  createAt  from status_bj_2013  where
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

'''
    createAt=sqlExec(sql_Query1)
    createAt.sort()
    return createAt

def load_weibo_num_from_databaseConsiderTime():
    createAt=loadCreateAt()
#
#    
    startTime=datetime.date(2013,1,1)
    endTime=datetime.date(2013,12,31)
    aDay=datetime.timedelta(days=1)
    days_that_we_donot_have=set()

    oneYear=[]
    while startTime <= endTime:
        oneDay=[]
        for item in createAt:
            if item[0].date() ==  startTime:
                
                oneDay +=[item]
                test= item[0].date()
                
        if test == startTime:                 
            oneDay_count=[]
            for i in range(0,24):
                onehour=[]
                for item in oneDay:
                    if item[0].hour == i:
                        onehour+= [item[0]]
                onehour_num = len(onehour)
                oneDay_count+= [onehour_num]
        
            oneYear += [(startTime,oneDay_count)]
        else:
            
            days_that_we_donot_have.add(startTime) 
            
        startTime += aDay
    return oneYear,days_that_we_donot_have

def getN():
    sql_Query1='''
select
hours,count(hours) as count
from
(select
hour(createAt) as hours
from status_bj_2013) as temp
group by
temp.hours
'''       
    hh = sqlExec(sql_Query1)    
    N=[item[1]/365 for item in hh]    
    return N
      

def getweekNUm():
    createAt=loadCreateAt()
    temp=[]
    week_num=[]
    for item in createAt:
        temp.append(item[0].weekday())
    for i in set(temp):
        print temp.count(i)/(365/7),'week:',i
    
        week_num.append(temp.count(i)/(365/7))  
        
    return week_num
   
def caclue_consider_time(oneYear,N):
    
    weibo_Ration =[]
    for item in oneYear:
        
        oneDay_num_consider_time = sum(item[1]/N)
        
        weibo_Ration += [[item[0]]+[oneDay_num_consider_time] ]
    return weibo_Ration
    
 
   
#------------------------------load kouzhao shuju --------------------------------------
def load_kouzhao_num():
    SQL_Query2='''
    select createAt,count(createAt) as daycot from
    (
    SELECT date(createAt) as createAt from kz_bj_2013_nodup  where
    
       text not like '%%%%http%%%%'
         and text not like '%%%%url%%%%'
         and text not like '%%%%【%%%%】%%%%'
         and text not like '%%%#%%%#%%%'
           and text like '%%%%%空气%%%%%%'
         and loc like '%%%%北京%%%%'
          and source not like '%%%%时光机%%%'
      #########filter       
         and isRetweet = 0
         ###23333
     
       ) as temp 
     
    group by  createAt
    
    '''
    kouzhao_num=sqlExec(SQL_Query2)
  
    
    return smoothYearDataTime_weioNum(kouzhao_num)

def loadYYFILE(filename):
    XMKQWR=csv.reader(file(filename,'r'))
    XMKQWR=list(XMKQWR)
    startTime=datetime.date(2013,1,1)
    endTime=datetime.date(2013,12,31)
    aDay=datetime.timedelta(days=1)
    daylist=[]
    
    while startTime <= endTime:

        good,bad,other=0,0,0

#        print 'start:',startTime
        
        for item in XMKQWR:
            
            temp=item[0].split('-')
            temp=[string.atoi(i) for i in temp]
            date=datetime.date(*temp)
#            print date,'@@'
#            break
 
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




# ----------------------WM number ----------------------------------------------
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
     and  text not like '%%%http%%%%'
    ) as temp
    group by createAt
    
    
    '''
    KQWR_data=sqlExec(sqL)
    return smoothYearDataTime_weioNum(KQWR_data)
###############################weibo with yuyi ####################################

def load_weibo_yuyi_result():
    reader=csv.reader(file('data/result.csv','rb'))
    
    data=[]
    for line in reader:
        data +=[line]
    print '-------weibo_yuyi_result item:----------'
    for item in data[0]:
        print item    
    del data[0]
    
    for item in data:
        item[0]=datetime.datetime.strptime(item[0],'%Y-%m-%d')
        item[1]=string.atoi(item[1])
        item[2]=string.atoi(item[2])
        item[3]=string.atoi(item[3])
    return data


def load_weibo_ration():
    
    N=getN()
    oneYear,days_that_we_donot_have=load_weibo_num_from_databaseConsiderTime()
    N=np.array(N,dtype=np.float)
    oneYear=np.array(oneYear)
    weibo_Ration=caclue_consider_time(oneYear,N)
    print len(weibo_Ration),'weiboRation'
    weibo_Ration,day_that_we_donot_have=smoothYearDataTime_weioNum(weibo_Ration)
    print len(weibo_Ration),'weiboRation'
    return weibo_Ration,days_that_we_donot_have

#load pm2.5in data----------------------------------------------
def loadPM2_5inFile(fname):
    bk=xlrd.open_workbook(fname)
    try:
        sh = bk.sheet_by_name("sheet")
    except:
        print "no sheet in %s named Sheet1" % fname
        
    nrows = sh.nrows
#    ncols = sh.ncols
    
#    print "nrows %d, ncols %d" % (nrows,ncols)
      
    row_list = []
    for i in range(1,nrows):
        row_data = sh.row_values(i)
#        print sh.cell(i,20).value

        date_value = xlrd.xldate_as_tuple(sh.cell(i,20).value,bk.datemode) 
        
        row_data[20]= datetime.date(*date_value[:3])
#        print row_data[1]
        row_list.append(row_data)
    return row_list

def getPm2_5inData():      
    fname='data/bj_2013_PM2.5Inn.xls'  
    loadedData = loadPM2_5inFile(fname)
    loadedData=np.array(loadedData)
    loadedData=loadedData[:,[0,12,13,20]]
    
    Pm2_5in = []
    startTime=datetime.date(2013,1,1)
    endTime=datetime.date(2013,12,31)
    aDay=datetime.timedelta(days=1)
    dayLoss_Pm2_5in=set()
    while startTime <= endTime:    
        temp=filter(lambda x: x[3]==startTime,loadedData)
        temp=np.array(temp)
        try:
            Pm2_5in.append( [startTime]+list(np.mean(temp[:,[0,1,2]],axis=0)) )
        except: 
            dayLoss_Pm2_5in.add(startTime)
            Pm2_5in.append([startTime]+['#_#','#_#','#_#'])
        startTime+=aDay
    return Pm2_5in,dayLoss_Pm2_5in  

def process_weather_data2(weather_data):
 
    for item in weather_data:
        item[4]=item[4][1]
#        print item[4]
    
#    chuli   fengli    
    try:
        for item in weather_data:
#            print item
#            temp = item[1] - item[2]
#            temperatuer_high += [item[1]]
#            temperature_low += [item[2]]
#            temperatureDelta += [temp]
#            print item[5]

            for i in range(len(item[5])):
                if item[5][0]:
                    item[5][0] = 6
                if item[5][1]:
                    item[5][1] = 5
                if item[5][2]:
                    item[5][2] = 4
                if item[5][3]:
                    item[5][3] = 7
                if item[5][4]:
                    item[5][4] = 3
            item[5] = np.max(item[5])
#            wind_power += [item[5]]
    except:
        pass

    weather_Feture=[]
    for item in weather_data:
#        print item[5]
        weather_Feture+=[ [item[0]]+[item[1]]+[item[2]] +[item[1]-item[2]]+item[3]+[item[4]]+[item[5]]   ]
    return weather_Feture





    

############ excel fuction######################################################  




if __name__ == '__main__':


    
    
    weather_data=process_loadedFile()
    BJ_weather_data=process_weather_data2(weather_data)
    BJ_weibo_yuyi_result=load_weibo_yuyi_result()    

#    BJ_kouzhao_num,BJ_kouzhao_ZWRO_Days = load_kouzhao_num()

    BJKZ_yuyiResult= loadYYFILE('data/BJKZ_sql_pre_data.csv')
    
    BJKZ_yuyiResult,BJKZ_yuyiResult_dayloss=smoothYearDataTime_weioNum(BJKZ_yuyiResult)
    BJKZ_yuyiResult =np.array(BJKZ_yuyiResult)



    BJ_Index=np.array(load_index2())   

    dateThatDonotUse=set()
    
    dateThatDonotUse.add(datetime.date(2013,1,12))
    dateThatDonotUse.add(datetime.date(2013,1,13))
    dateThatDonotUse.add(datetime.date(2013,1,14)) #确实在说空气污染很严重，确实空气污染很严重，官方指数不准
    dateThatDonotUse.add(datetime.date(2013,1,15)) #确实在说空气污染很严重，（雪）确实空气污染很严重（爆表），官方指数不准
    dateThatDonotUse.add(datetime.date(2013,1,29))
    dateThatDonotUse.add(datetime.date(2013,1,30)) #确实在说空气污染很严重，确实空气污染很严重，官方指数不准
    dateThatDonotUse.add(datetime.date(2013,1,31)) #在说空气污染，不过也有很多是评头论足
    dateThatDonotUse.add(datetime.date(2013,2,24)) #遮天元宵节，氮污染还是蛮严重的
    dateThatDonotUse.add(datetime.date(2013,2,28)) #确实在说空气污染很严重，确实空气污染很严重（爆表），官方指数不准



    day_loss =  dateThatDonotUse

    week_num=getweekNUm()
    








#with open('weibonum.csv','wb') as csvfile:
#    swriter=csv.writer(csvfile,delimiter=',',quotechar=',', quoting=csv.QUOTE_MINIMAL)
#    for item in weibo_num:
#        swriter.writerow(item)
    
    

    
    
    
    
    
    
    
    
    