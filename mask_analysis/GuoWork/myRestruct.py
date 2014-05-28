# -*- coding: utf-8 -*-
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import numpy as np
import jieba
import jieba.posseg as pseg
from pytagcloud import create_tag_image, make_tags, create_html_data
##from pytagcloud.lang.counter import get_tag_counts
import simplejson
import pygame
##---------------------------------------load user dict and stopwords-------------------
def My_make_word_could(fileStr,outPNGStr):

    jieba.load_userdict("ap_dict.txt")
    STOP_WORD = set()
    stopword_file = open("stopwords.txt")
    for each_line in stopword_file:
        each_line_list = pseg.cut(each_line)
        for elem in each_line_list:
            STOP_WORD.add(elem.word)
        STOP_WORD.add(each_line.strip().decode('utf-8'))
    stopword_file.close()

    ##-----------------------------------------------------cut and cul wrod freq------------------------------------
    word_freq = {}
##    fileStr = "kouzhao.txt"
    raw_file = open(fileStr)
    for line in raw_file:
        seg_list = pseg.cut(line)
        for ele in seg_list:
            words = ele.word.strip()
    ##        print words in STOP_WORD
            if ((ele.flag == 'n' or ele.flag == 'a' ) and (words not in STOP_WORD)):
                if(word_freq.has_key(words)):
                    word_freq[words] += 1
                else:
                    word_freq[words] = 1
    raw_file.close()

    ##---------------------------------------------sort the result--------------------------
    paixu= sorted(word_freq.iteritems(), key=lambda d:d[1], reverse = True)
    paixu_tiqu=paixu[0:25]
    print "over"


    ##for (k,v) in word_freq.items():
    ##    if v==1:
    ##        del word_freq[k]
    ##    print k,v
    ##for (k,v) in word_freq.items():    
    ##    print k,v
    ##for item in word_freq.keys():
    ##    print item
    ##for (k,v) in (dict (paixu_tiqu)).items():
    ##    print k,v
    ##--------------------------------------------make word cloud --------------------------------   
    tags = make_tags(dict(paixu_tiqu))
    ##print tags
##    outPNGStr = 'kouzhao.png'
    create_tag_image(tags, outPNGStr, size=(2000, 1600), fontname='haokan.ttf',fontzoom=4)
    print "all over"

#------------------------------------- use ---------------------------------------------

fileStr = "0.txt"
outPNGStr = 'kouzhao.png'
My_make_word_could(fileStr,outPNGStr)
##for i in range(2):   
##    fileStr =str(i) + '.txt'
##    outPNGStr = str(i) + '.png'
##    My_make_word_could(fileStr,outPNGStr)



















