# -*- coding: utf-8 -*-
"""
Created on Fri May 09 15:54:41 2014

@author: zqh
"""
import numpy as np
import pylab as plt

good=Pm_DataSet.dataSet

bad_in_day_loss=Pm_DataSet.filter_data_in_day_loss

good_date = good[:,0]
good_weibo_num = good[:,9]
good_wuhan_level = good[:,-1]


bad_date = bad_in_day_loss[:,0]
bad_weibo_num = bad_in_day_loss[:,9]
bad_wuhan_level = bad_in_day_loss[:,-1]




print len(good),len(bad_in_day_loss)

plt.scatter(good_date,good_weibo_num,c='g',marker='o', alpha=0.7,label='good')
plt.scatter(bad_date,bad_weibo_num,c='r',marker='o', alpha=0.7,label='bad')
plt.xlabel('date')
plt.ylabel('weibo num')
plt.legend(loc = 'upper right')
plt.show()




plt.scatter(good_date,good_wuhan_level,c='g',marker='o', alpha=0.7,label='good')
plt.scatter(bad_date,bad_wuhan_level,c='r',marker='o', alpha=0.7,label='bad')
plt.xlabel('date')
plt.ylabel('wuhan_level')
#plt.legend(loc = 'upper right')
plt.show()