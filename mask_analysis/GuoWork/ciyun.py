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

jieba.load_userdict("ap_dict.txt")


STOP_WORD = set()
stopword_file = open("stopwords.txt")
for each_line in stopword_file:
    each_line_list = pseg.cut(each_line)
    for elem in each_line_list:
        STOP_WORD.add(elem.word)
    STOP_WORD.add(each_line.strip().decode('utf-8'))
stopword_file.close()

##print STOP_WORD
##print '-------------'
##for elem in STOP_WORD:
##    print elem
##print '-------------'
word_freq = {}
raw_file = open("app.txt")
for line in raw_file:
    seg_list = pseg.cut(line)
    for ele in seg_list:
        words = ele.word.strip()
##        print words in STOP_WORD
        if ((ele.flag == 'n' or ele.flag == 'an' or words.encode('utf-8','ignore')=='薛蛮子' or ele.flag == 'nr') and (words not in STOP_WORD)):
            if(word_freq.has_key(words)):
                word_freq[words] += 1
            else:
                word_freq[words] = 1
##print word_freq
raw_file.close()
paixu= sorted(word_freq.iteritems(), key=lambda d:d[1], reverse = True)
paixu_tiqu=paixu[0:25]
print "over"
##for (k,v) in word_freq.items():
##    print k,v
##print word_freq
##for (k,v) in (dict (paixu_tiqu)).items():
##    print k,v 
tags = make_tags(dict(paixu_tiqu))
##print tags
create_tag_image(tags, 'app1.png', size=(2000, 1600), fontname='simhei.ttf',fontzoom=4)

print "all over"
