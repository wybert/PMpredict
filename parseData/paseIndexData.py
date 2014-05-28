# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 21:22:16 2014

@author: zqh
"""


import urllib2
from bs4 import BeautifulSoup
import urllib    
import csv

def parOnePage(url):

	page = urllib2.urlopen(url)
	html_doc = page.read()
	#print html_doc
 
	soup = BeautifulSoup(html_doc.decode('utf-8','ignore'))
	doc = soup.findAll('tr', height="30")

	dataCollect=[]
	for row in doc:
	    text = ''.join(row.findAll(text=True))
	    data = text.strip()
	    dataCollect.append(data.split())
	return dataCollect
    
 

def gennerUrl(city,startdate,enddate,page):

    url = 'http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp'  

    values = {'city':city,'startdate':startdate,'enddate':enddate,

			'page':str(page)}   

    data = urllib.urlencode(values)
    url2 = url+'?'+data

    return url2
    

def getAllPage(city,startdate,enddate):
    allPageData=[]

    for page in range(1,6):
        print page

        url = gennerUrl(city,startdate,enddate,page)
        OnePageData = parOnePage(url)
        del OnePageData[0]
        del OnePageData[0]
        allPageData += OnePageData
#        break	
    return allPageData


cityConfig=[r"上海市",r"厦门市"]
filename=["shanghai","xiamen"]

startdate,enddate=r"2014-01-01",r"2014-05-15"


for city,name in zip(cityConfig,filename):
    cityData  = getAllPage(city,startdate,enddate)
    print name
    with open(name+'.csv', 'wb') as csvfile:
        swriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in cityData:
            swriter.writerow(item)
    






































