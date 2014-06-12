# -*- coding: utf-8 -*-
"""
Created on Mon Jun 09 14:52:34 2014

@author: zqh
"""
import numpy as np
import string
import time
import urllib2
from bs4 import BeautifulSoup
import urllib    
import csv
import datetime

def parOnePage(url):
    page = urllib2.urlopen(url)
    html_doc = page.read()
#    print html_doc
 
    soup = BeautifulSoup(html_doc.decode('utf-8','ignore'))
 
    doc = soup.findAll('tr', class_="no-metars")
#    print doc

    dataCollect=[]
    for row in doc:
        
        cell_list=row.findAll('td')
        row_contain=[]
        for cell in cell_list:            
            text = ''.join(cell.findAll(text=True)) 
#            print text
            data = text.strip()
            row_contain.append(data.split())
        dataCollect.append(row_contain)
    return dataCollect
    


def gennerUrl(city,date):

    url1 = 'http://www.wunderground.com/history/airport/'
    url4=  "/DailyHistory.html?"
    url =url1+city+'/'+date +url4

    return url
    

def getAllPage(city,startdate,enddate):
    AllDayData=[]
    aDay =datetime.timedelta(days=1)
    while startdate < enddate:
        print startdate
        date=startdate.strftime('%Y/%m/%d')
        url = gennerUrl(city,date)
        try:
            oneDayData = parOnePage(url)
        except Exception, e:
            print Exception,':',e
            
            print '#_#'
            time.sleep(10)
            oneDayData = "#_#"
        print len(oneDayData)
        AllDayData.append(oneDayData)
#        break
        startdate += aDay
    return AllDayData



def calu_wind_dir(wind_dir_daylist):
    
    fengxiangSet=["North", "NNE", "NE", "ENE", "East", "ESE", "SE", "SSE", "South", "SSW", "SW", "WSW", "West", "WNW", "NW", "NNW"]
    fengxiangSet=set(fengxiangSet)
#    print fengxiangSet
    
    wind_dir_dict = {}
    for item in fengxiangSet:
        wind_dir_dict[item] = 0        
    Variable = 0 
#    print 'here:',wind_dir_daylist
    
    for item in wind_dir_daylist:
#        print item
        if item in fengxiangSet:
            if(wind_dir_dict.has_key(item)):
                wind_dir_dict[item] += 1
           
        elif item == 'Variable':
            Variable += 1
        else:
            print '#_#',item
    
#    for (k,v) in wind_dir_dict.items():    
#        print k,v
          
    wind_dir_values = wind_dir_dict.values()
    wind_dir_values = np.array(wind_dir_values)    
#    wind_dir_shang = wind_dir_values.var()*(1+Variable)
    wind_dir_shang = wind_dir_values.var()
    
    return wind_dir_shang

def calu_weather_data(weather_daylist):
    
    weather = ["Snow","Haze","Fog","Blowing","Freezing","Thunderstorm","Rain","Dust",
    "Clouds","Grains","Light","Clear","Overcast","Cloudy","Sand",
    "Thunderstorms","Showers","Mist","Drizzle"]
    
    weather_dict = {}
    for item in weather:
        weather_dict[item] = 0        
    Variable = 0 

    for item in weather_daylist:
        if item in weather:
            if(weather_dict.has_key(item)):
                weather_dict[item] += 1
           
        elif item == 'Variable':
            Variable += 1
        else:
            print '#_#',item
    
    for (k,v) in weather_dict.items():    
        print k,v
          
    weather_values = weather_dict.values()
    
    return weather_values
def preprocessingWeatherData_aday(temperature,humid,pressure,wind_speed,wind_dir,weather):
#    print temperature
    temperature=[string.atof(i) for i in temperature]        
    temperature = np.array(temperature)  
    temperature_mean=np.mean(temperature)     

    humid=[string.atof(i) for i in humid]        
    humid = np.array(humid)  
    humid_mean=np.mean(humid)     
    
    pressure=[string.atof(i) for i in pressure]        
    pressure = np.array(pressure)  
    pressure_mean=np.mean(pressure)     

    temp=[]
    for item in wind_speed:
        if item != 'Calm':
            temp.append(string.atof(item))
        else:
            temp.append(0)
           
    temp = np.array(temp)  
    wind_speed_mean=np.mean(temp)     

    wind_dir = calu_wind_dir(wind_dir)
  
    weather = calu_weather_data(weather)
    
    adaylist= [temperature_mean,humid_mean,pressure_mean ,wind_speed_mean,wind_dir,
                ] + weather
#    print '^^'
#    print adaylist
    return adaylist

def preprocessingWeatherData(downloadedData,startdate,aDay):
    i=0
    preprocessedWeatherData=[]
    for adaylist in  downloadedData:
        
        print startdate
        temperature=[]
        humid=[]
        pressure=[]
        wind_speed=[]
        wind_dir=[]
        weather=[]
        for rowlist in adaylist:
            if len(rowlist) == 12:
                pass
            elif len(rowlist) == 13:
                temperature.append(rowlist[1][0])
                humid.append(rowlist[4][0].strip("%"))
                pressure.append(rowlist[5][0])
                wind_speed.append(rowlist[8][0])
                wind_dir.append(rowlist[7][0])
                for item in rowlist[12]:
                    weather.append(item)
                
                
            else:
                print "#_#"
    #    temperature_mean=np.mean(temperature) 
#        print '^_^'
        adaylist = preprocessingWeatherData_aday(temperature,humid,pressure,wind_speed,wind_dir,weather)        
        
        preprocessedWeatherData.append(startdate+adaylist)
        
        
        if i>=3:
            break
        i+=1
        print "-"*30
        
        startdate+=aDay
    print preprocessedWeatherData    
    return preprocessedWeatherData
    




#  beijing
city="ZBAA"

timeDeta=datetime.timedelta(days = 10)
startdate=datetime.date(2013,1,1)
enddate=datetime.date(2013,12,31)

while startdate<=enddate:
    print startdate
    beijingweatherdata=getAllPage(city, startdate, startdate+timeDeta)
    print 'over1'
    startdate+=timeDeta


#    
#for i in range(1,12):
#    
#    print i
#    
#    print '--------------------get one month data-------------------------'
#    print startdate,enddate
#    break
#
#
#
#
#
#startdate=datetime.date(2013,1,1)
#enddate=datetime.date(2013,12,31)
#aDay=datetime.timedelta(days=1)   
#preprocessedWeatherData = preprocessingWeatherData(beijingweatherdata,startdate,aDay) 
   


























