# -*- coding: utf-8 -*-
"""
Created on Fri May 16 21:30:25 2014

@author: zqh
"""

import urllib2
from bs4 import BeautifulSoup

#import urllib   
#import chardet
 
import csv
#url = r"http://lishi.tianqi.com/xiamen/201401.html"


def paseOneMonth(url):
    page = urllib2.urlopen(url)
    html_doc = page.read()
#    print chardet.detect(html_doc)
      
    soup = BeautifulSoup(html_doc.decode('GB2312','ignore'))
    
    doc = soup.find('div', class_ = "tqtongji2" )
    #print doc
    tablelist = doc.findAll('ul')
    
    dataCollect=[]
    for row in tablelist:
        
        text = ''.join(row.findAll(text=True))
        data = text.strip()
        dataCollect.append(data.split())
    return dataCollect
def gennnerUrl(city,month):
    
    url = r"http://lishi.tianqi.com/%s/2014%02d.html"%(city,month)
    print url
    return url


def downloadAllMonth(city):
    cityWeather=[]
 
    for month in range(1,5):
        
#        gennnerUrl(city,month)  
        dataCollect = paseOneMonth( gennnerUrl(city,month)  )
        del dataCollect[0]
        cityWeather += dataCollect 

        
#        break
    return cityWeather
        


filename=["shanghai","xiamen"]

for city in filename:
    cityWeather = downloadAllMonth(city)    
#    print name
    with open(city+'weather.csv', 'wb') as csvfile:
        swriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in cityWeather:
            swriter.writerow(item)































    
    