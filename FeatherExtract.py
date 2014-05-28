# -*- coding: utf-8 -*-
"""
Created on Thu Apr 03 19:02:51 2014

@author: zqh
"""

import numpy as np
import datetime
from loadData import *

##创建一个归一化计算的函数
def MaxMinNorm(before,newMin,newMax):
    
    after=[(float(i)-min(before))*(newMax-newMin)/(max(before)-min(before))+newMin 
    for i in before]
    return after
    
    


class PmDataSet():
    def __init__(self,weather_data,weibo_yuyi_result,index2,kouzhao_num,WM_num,weibo_Ration,day_loss,week_num):
        self.weibo_yuyi_result = weibo_yuyi_result
        self.index2 = index2
        self.kouzhao_num = kouzhao_num
        self.day_loss = day_loss
        self.weibo_Ration = weibo_Ration
        self.week_num=week_num
        self.WM_num=WM_num
#        self.Pm2_5in=Pm2_5in

  #--------------------weather---------------------------
     
        temperatureDelta = []
        wind_power=[]
        temperatuer_high = []
        temperature_low = []
        
        try:
            for item in weather_data:
    #            print item
                temp = item[1] - item[2]
                temperatuer_high += [item[1]]
                temperature_low += [item[2]]
                temperatureDelta += [temp]
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
                wind_power += [item[5]]
        except:
            pass
    
        weather_Feture=[]
        for item in weather_data:
            weather_Feture+=[ [item[0]]+[item[1]]+[item[2]] +[item[1]-item[2]]+item[3]+item[4]+[item[5]]   ]
        
        weather_Feture=np.array(weather_Feture)
        
    
        #-----------------------weibo-------------------------------------------
        weibo_yuyi_Feture=np.array(self.weibo_yuyi_result)
        weibo_yuyi_Feture=weibo_yuyi_Feture[:,1:]
        
       #----------------------kouzhao --------------------------------------
        kouzhao_num = np.array(self.kouzhao_num)
        kouzhao_num = kouzhao_num[:,1:]
    
        # --------------------WM_num-------------------------
        WM_num=np.array(WM_num)
        WM_num=WM_num[:,1:]


        # ----------------------------weio ration------------------------------

        weibo_Ration=np.array(self.weibo_Ration)
        weibo_Ration = weibo_Ration[:,1:]






    #    ---------------------------折叠  -------------------------------------
        data=np.hstack((weather_Feture,weibo_yuyi_Feture,kouzhao_num,WM_num,weibo_Ration))
        
        #----------------------target-----------------------------
        
    #   
    #    target_level=[]
    #    target=[]
    #    for item in index2:
    #        target += [[item]]
    #        if item <= 35:
    #            target_level += [['good']]
    #        elif item > 35 and item <= 75:
    #            target_level += [['moderate']]
    #        elif item >75 and item <= 115:
    #            target_level += [['unhealthy_mild']]
    #        elif item >115 and item <= 150:
    #            target_level += [['unhealthy_moderate']]
    #        elif item > 150 and item <=250:
    #            target_level += [['unhealthy_serious']]
    #        elif item > 250:
    #            target_level += [['unhealthy_verySerious']]
    #            
    #    for item in index2:
    #        target += [[item]]
    #        if item <= 35:
    #            target_level += [[1]]
    #        elif item > 35 and item <= 75:
    #            target_level += [[2]]
    #        elif item >75 and item <= 115:
    #            target_level += [[3]]
    #        elif item >115 and item <= 150:
    #            target_level += [[4]]
    #        elif item > 150 and item <=250:
    #            target_level += [[5]]
    #        elif item > 250:
    #            target_level += [[6]]           
    #    for item in target_level:
    #        print item    

        #index=np.array(index1)
    #    target_level=np.array(target_level)

        index2=np.array(self.index2)
        target = index2[:,1:]
#        target = self.Pm2_5in[:,:1]
    
#        print len(data[0]),len(target[0])
        

        self.dataSet_Write_to_R=np.hstack((data,target))



        wealth_item =['time','temperatuer_high','temperature_low','temperatureDelta',
                     u'晴',u'云',u'阴',u'雨',u'雾',u'霾',u'雪',u'沙',u'雷',
                     u'无持续风向',u'北风',u'东北风',u'南风',
                     'wind_power']
        weibo_yuyi_item=['good','bad','other']
        kouzhao_num_item =['kouzhaoWeiboNum']
        WM_num_item =["WM_num"]
        weibo_Ration_item = ['weibo_Ration']
        target_item=['target']
        item_name = wealth_item + weibo_yuyi_item + kouzhao_num_item+ WM_num_item + weibo_Ration_item+ target_item
        self.item_name=item_name



#       [0,1,2,4,5,6,7,8,9,13,14,15,17,18,19,20,21,22,24]


    def write_to_R(self):

        
        
        print len(self.item_name),'item_name'     
        
        print len(self.dataSet_Write_to_R[1]),'data'
        with open('R/dataSet_Write_to_R.csv', 'wb') as csvfile:
           swriter = csv.writer(csvfile, delimiter=',',quotechar=',', quoting=csv.QUOTE_MINIMAL)    
           swriter.writerow(self.item_name)
           for item in self.dataSet_Write_to_R:
               swriter.writerow(item)      

    def load_DataSet(self):
           
     

        
        
# consider weekdays
        for item in self.dataSet_Write_to_R:
            for i in range(7):
                if item[0].weekday()==i:
                    item[18]=item[18]/float(self.week_num[i])
                    item[19]=item[19]/float(self.week_num[i])
#                    item[20]=item[20]/float(self.week_num[i])
#                    item[21]=item[21]/float(self.week_num[i])
#                    item[22]=item[22]/float(self.week_num[i])



##   add kouzhao num
#
#        for item in self.dataSet_Write_to_R:
#            for i in range(7):
#                if item[0].weekday()==i:
##                    item[18]=item[18]/float(self.week_num[i])
##                    item[21]=item[21]/float(self.week_num[i])
#                    item[19]=item[19]+item[21]/float(self.week_num[i])
                            



        item_name = self.item_name
        item_name = np.array(item_name)

#        fetrue_select_num = [0,4,7,8,9,13,15,17,18,19,21,22,23]
        fetrue_select_num = [0,1,2,4,5,6,7,8,9,13,14,15,17,18,19,20,21,24]
#        fetrue_select_num = range(24)
        selectedFetureName = item_name[fetrue_select_num]
        
        print "selected feture set:"
        print "##############################################"

        for i,item in enumerate(selectedFetureName) :
            print i,item

        print "##############################################"


        fetureSelected_dataSet = self.dataSet_Write_to_R[:,fetrue_select_num]
        
        
    #    fetureSelected_dataSet = self.dataSet_Write_to_R[:,[0,4,7,8,9,17,18,19,21,22]]
        
#        kou zhao  and  index
#        fetureSelected_dataSet = self.dataSet_Write_to_R[:,[0,18,19,23]]
    
#        fetureSelected_dataSet = self.dataSet_Write_to_R[:,[0,4,7,8,9,13,15,17,23]]
    #    fetureSelected_dataSet = self.dataSet_Write_to_R[:,[0,4,7,8,9,13,15,17,21,22]]
 


    #------------------time facotor -----------------------------------------------
        
#        dateEnd = datetime.date(2013,6,30)
#        dateStart = datetime.date(2013,8,1)

        dataSet_filter_by_time = [item for item in fetureSelected_dataSet if 
#               (item[0] <=dateEnd or (item[0] >=dateStart)) and
                item[0] not in self.day_loss
#                and ( item[19]>=0 and item[19] <= 500)               
               ]
        
#        print len(dataSet_filter_by_time)
#        for item in dataSet_filter_by_time:
#            print item

        dataSet_filter_by_time = np.array(dataSet_filter_by_time)
              

# to use analysis another data

#        self.fetureSelected_dataSet=fetureSelected_dataSet
#
#        filter_data_in_Jun = [item for item in fetureSelected_dataSet if 
#               (item[0] > dateEnd and (item[0] < dateStart))
#               ]
#
#        self.filter_data_in_Jun = np.array(filter_data_in_Jun)
#
#
#        filter_data_in_day_loss = [item for item in fetureSelected_dataSet if 
#                item[0]  in self.day_loss
#               ]
#        
#        self.filter_data_in_day_loss = np.array(filter_data_in_day_loss)




## consider time delta
#        timedeta=[]
##        detaAll=[]
#        for i in range(len(dataSet_filter_by_time)-1):
#            delta = dataSet_filter_by_time[i+1][2]-dataSet_filter_by_time[i][2]
##            delta2 = dataSet_filter_by_time[i+1][1:]-dataSet_filter_by_time[i][1:]
#            
##            detaAll+= [np.hstack((dataSet_filter_by_time[i+1][:1],delta2))]
#
#            
#            
#            timedeta +=[ [delta]]
#            
#        timedeta=np.array(timedeta)
##        detaAll =np.array(detaAll)
#        
#        
#        print len(dataSet_filter_by_time[1:,:-1]),len(timedeta)
#        dataConsiderTime = np.hstack((dataSet_filter_by_time[1:,:-1],timedeta,dataSet_filter_by_time[1:,-1:]))
#







        N=1
        num_Sample = len(dataSet_filter_by_time)-N+1
        dataSet = []
        for i in range(num_Sample):
            temp = dataSet_filter_by_time[i:i+N,:]
            temp.ravel()
            oneSample=[]
            for item in temp:
                oneSample += list(item)
    #        print temp
    #        break
            dataSet += [oneSample]
            
        dataSet = np.array(dataSet)
        self.dataSet = dataSet
       



        return dataSet,selectedFetureName
#        return np.array(sonsider_timedeta)
#        return dataConsiderTime
#        return detaAll
        
        
        ##--------------------------deal null---------------------------
    #    dataSet1=np.hstack((data,target))
    #    
    #    dataSet_del_null=[]
    #    for item in dataSet1:
    #        if item[24]!='null':
    #            dataSet_del_null+=[item]
    #            
    #    dataSet_del_null=np.array(dataSet_del_null)
    #    return dataSet_del_null

Pm_DataSet = PmDataSet(weather_data,weibo_yuyi_result,index2,kouzhao_num,WM_num,weibo_Ration,day_loss,week_num)

dataSet,selectedFetureName = Pm_DataSet.load_DataSet()
print dataSet.shape
#Pm_DataSet.write_to_R()
#
#Pm_DataSet.dataSet
#Pm_DataSet.filter_data_in_day_loss

