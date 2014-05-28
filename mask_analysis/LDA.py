# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 22:27:19 2014

@author: zqh
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 16:04:03 2014

@author: zqh
"""
from gensim import corpora, models
import jieba.posseg as pseg
import numpy as np
import csv



def load_STOP_WORD():
    STOP_WORD = set()
    stopword_file = open("stopwords.txt")
    for each_line in stopword_file:
        each_line_list = pseg.cut(each_line)
        for elem in each_line_list:
            STOP_WORD.add(elem.word)
        STOP_WORD.add(each_line.strip().decode('utf-8'))
    stopword_file.close()    
    return STOP_WORD

def get_MyCorpora(KZ_text):

    STOP_WORD= load_STOP_WORD()
    words=[]
    print "building my corpora..."
    for item in KZ_text:
        for doc in item: 
            doc_list=[]
            seg_list = pseg.cut(doc)
            for ele in seg_list:
                word = ele.word.strip()        
                if ((ele.flag == 'n' or ele.flag == 'a'  ) and (word not in STOP_WORD)):
                    doc_list += [word]
            words.append(doc_list)
    dic = corpora.Dictionary(words)

    dic.save('mydic.dict')
    corpus = [dic.doc2bow(text) for text in words]
    corpora.MmCorpus.serialize('mycorpora.mm', corpus)

    print "build my corpora sucessfully!"

    return corpus,dic



def get_topics_by_lda(N):

    corpus = corpora.MmCorpus('mycorpora.mm')
    dic = corpora.Dictionary.load('mydic.dict')
    corpus=list(corpus)
    #  tdidf used
#    print "tfidf transforming..."
#    tfidf = models.TfidfModel(corpus)
#    corpus_tfidf = tfidf[corpus]
#    print "tfidf transform over..."
#    print corpus_tfidf

    # lda topic   

    print "lda transforming..."
    LDA = models.LdaModel(corpus, id2word=dic, num_topics=N,eval_every=11) 
    ldaout=LDA.print_topics(N)
    print "lda transform over..."
    for i in range(N):
        print "------------------------topic",i,"-----------------------------"
        print ldaout[i]

    # lda app

    corpus_lda = LDA[corpus]
    return corpus_lda

def my_save_result(corpus_lda,KZ_text,N):

    #  wirte to analysis
    print "writing my topic_result..."
#    sentence_topic = np.array(list(corpus_lda))   
    topic = []
    
    for item in corpus_lda:
        one=[]
        for j in item:
            one += [j[1] ]      
        for i in range(len(one)):        
            if one[i] == np.max(one):
                topic += [[item[i][0]]]
                break
    
    
#    for i in range(len(sentence_topic)):    
#        one = sentence_topic[i,:,1]
#        for j in range(len(one)):
#            if one[j] == np.max(one):
#                topic+=[[j]]
#                break

    topic = np.array(topic)
    print len(topic),len(KZ_text)
    to_write=np.hstack((topic,KZ_text))
    
    
    for i in range(N):
        topic_text = [ item[1] for item in to_write if item[0] == str(i)]       
        output1=open(str(i)+'.txt', 'wb')
        for item in topic_text:         
            output1.write(item)
        output1.close()  
     
  
 
    with open('topic_result.csv', 'wb') as csvfile:
        swriter = csv.writer(csvfile, delimiter=' ',quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for item in to_write:
            swriter.writerow(item)
    print "writing my topic_result over ! "


#corpus,dic = get_MyCorpora(KZ_text_sample)

N=100

corpus_lda = get_topics_by_lda(N)

my_save_result(corpus_lda,KZ_text_sample,N)




i=0
for doc in corpus_lda:
    print doc
    i += 1
    if i >10:
        break








## -----------------------------------------------------------------------
## 相似度查询，可以查询到相关的主题
#   
#index = similarities.MatrixSimilarity(lsi[corpus])
#query = "雾霾"
#query_bow = dic.doc2bow(list(jieba.cut(query)))
#print query_bow
#query_lsi = lsi[query_bow]
#print query_lsi
#
#
#
#sims = index[query_lsi]
#print list(enumerate(sims))
#sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
#print sort_sims
#









