# -*- coding: utf-8 -*-
"""
Created on Thu Apr 03 19:02:51 2014

@author: zqh
"""

import numpy as np
from loadData import *

##创建一个归一化计算的函数
def MaxMinNorm(before,newMin,newMax):
    
    after=[(float(i)-min(before))*(newMax-newMin)/(max(before)-min(before))+newMin 
    for i in before]
    return after

def normlize_data(mergered_data,week_num,poplation):
# cosider poplation

#    mergered_data[:,[15,16,17,18,19,20]] = mergered_data[:,[15,16,17,18,19,20]]/poplation


# consider weekdays
    for item in mergered_data:
        for i in range(7):
            if item[0].weekday()==i:
                item[15]=item[15]/float(week_num[i])
                item[16]=item[16]/float(week_num[i])
                item[17]=item[17]/float(week_num[i])
                item[18]=item[18]/float(week_num[i])
                item[19]=item[19]/float(week_num[i])
                item[20]=item[20]/float(week_num[i])

# gui yi hua   
#    temp= mergered_data[:,[15,16,17,18,19,20]] 
#
#    mergered_data[:,[15,16,17,18,19,20]] = (temp- np.min(temp,axis=0))/(np.max(temp,axis=0) -np.min(temp,axis=0) )

    return mergered_data
    


def transIndex2Levels(index):
          
    target_level=np.zeros(index.shape,dtype=int)

    for i in range(len(index)):
        if index[i][1] <= 100:
            target_level[i][1] = 1

        elif index[i][1] > 100 and index[i][1] <= 300:
#            print '#_#'
            target_level[i][1] = 2
        elif index[i][1] > 300:
            target_level[i][1] = 3 
#    print '######################################'  
#    for item in target_level:
#        print item    
#    print '######################################'    
#    for item in index:
#        print item
#    print '######################################'  

    return target_level


    
def merger_data(weather_Feture,weibo_yuyi_result,kouzhao_num,index):


#--------------------weather---------------------------
    
    weather_Feture=np.array(weather_Feture)
    
    #-----------------------weibo-------------------------------------------
    weibo_yuyi_result=np.array(weibo_yuyi_result)
    weibo_yuyi_result=weibo_yuyi_result[:,1:]
    
   #----------------------kouzhao --------------------------------------
    kouzhao_num = np.array(kouzhao_num)
#    print '^_^',kouzhao_num.shape
    kouzhao_num = kouzhao_num[:,1:]
  
#    ---------------------------折叠  -------------------------------------
    data=np.hstack((weather_Feture,weibo_yuyi_result,kouzhao_num))
    
    #----------------------target-----------------------------
   


    target = index[:,1:]
    dataSet_Write_to_R=np.hstack((data,target))
    
    return dataSet_Write_to_R



#normlized_data = normlize_data(mergered_data,week_num)


def write_to_R(item_name,dataSet_Write_to_R):


    print len(item_name),'item_name'     
    
    print len(dataSet_Write_to_R[1]),'data'
    with open('R/dataSet_Write_to_R.csv', 'wb') as csvfile:
       swriter = csv.writer(csvfile, delimiter=',',quotechar=',', quoting=csv.QUOTE_MINIMAL)    
       swriter.writerow(item_name)
       for item in dataSet_Write_to_R:
           swriter.writerow(item)      


def featureSlect(mergered_data):


    wealth_item =['time','temperatuer_high','temperature_low','temperatureDelta',
                 u'晴',u'云',u'阴',u'雨',u'雾',u'霾',u'雪',u'沙',u'雷',
                 u'风向'
                 ,'wind_power']
    weibo_yuyi_item=['good','bad','other']
    kouzhao_num_item =['KZ_good','KZ_bad','KZ_other']   
    target_item=['target']
    item_name = wealth_item + weibo_yuyi_item + kouzhao_num_item+  target_item
    item_name = np.array(item_name)

    fetrue_select_num = [0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,21]
#    fetrue_select_num = range(len(item_name))
    
    global SELECTED_FETURE_NAME
    SELECTED_FETURE_NAME = item_name[fetrue_select_num]
    
    print "selected feture set:"
    print "##############################################"

    for i,item in enumerate(SELECTED_FETURE_NAME) :
        print i,item

    print "##############################################"
#    print fetrue_select_num
#    print mergered_data.shape

    fetureSelected_dataSet = mergered_data[:,fetrue_select_num]

    return fetureSelected_dataSet





def resample(fetureSelected_dataSet,day_loss):

# conside time factor
    dataSet_filter_by_time = [item for item in fetureSelected_dataSet if 
#               (item[0] <=dateEnd or (item[0] >=dateStart)) and
            item[0] not in day_loss
#                and ( item[19]>=0 and item[19] <= 500)               
           ]
    dataSet_filter_by_time = np.array(dataSet_filter_by_time)
    
    return dataSet_filter_by_time


def resample_cosider_before_days(resampled_data):
       
## consider time delta
#        timedeta=[]
##        detaAll=[]
#        for i in range(len(resampled_data)-1):
#            delta = resampled_data[i+1][2]-resampled_data[i][2]
##            delta2 = resampled_data[i+1][1:]-resampled_data[i][1:]
#            
##            detaAll+= [np.hstack((resampled_data[i+1][:1],delta2))]
#
#            
#            
#            timedeta +=[ [delta]]
#            
#        timedeta=np.array(timedeta)
##        detaAll =np.array(detaAll)
#        
#        
#        print len(resampled_data[1:,:-1]),len(timedeta)
#        dataConsiderTime = np.hstack((resampled_data[1:,:-1],timedeta,resampled_data[1:,-1:]))
#

    resampled_data=resampled_data[:,1:]
#    N=1
    N=3
    num_Sample = len(resampled_data)-N+1
    dataSet = []
    for i in range(num_Sample):
        temp = resampled_data[i:i+N,:]
        temp.ravel()
        oneSample=[]
        for item in temp:
            oneSample += list(item)
#        print temp
#        break
        dataSet += [oneSample]
        
    dataSet = np.array(dataSet)
    
    date =np.zeros((len(dataSet),1))
#    print date
    dataSet = np.hstack((date,dataSet))

    return dataSet


 
def loadDataSet(weather_data,weibo_yuyi_result,kouzhao_num,Index,week_num,day_loss,poplation):
    
    target=transIndex2Levels(Index)
    mergered_data = merger_data(weather_data,weibo_yuyi_result,kouzhao_num,target)
    normlized_data = normlize_data(mergered_data,week_num,poplation)  
    featureSlected_data = featureSlect(normlized_data) 
    resampled_data =  resample(featureSlected_data,day_loss)
    resampled_cosider_before_days = resample_cosider_before_days(resampled_data)
    
    
    return resampled_cosider_before_days
    

if __name__ == '__main__':
    beijing_pop=1297.46
    BJ_DataSet = loadDataSet(BJ_weather_data,BJ_weibo_yuyi_result,BJKZ_yuyiResult,BJ_Index,week_num,day_loss,beijing_pop)

#    xiamen_pop=190.92
#    XM_DataSet = loadDataSet(XM_Weather,XMKQWR_yuyiResult,XM_KZ_NUM,XM_Index,week_num,predict_dayloss,xiamen_pop)
#    
    shanghai_pop=1426.93
    
    SH_DataSet = loadDataSet(SH_Weather,SHKQWR_yuyiResult,SHKZ_yuyiResult,SH_Idex,week_num,predict_dayloss,shanghai_pop)

























