
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 15:43:09 2014

@author: zqh
"""
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
import pylab as plt
import datetime
from sklearn.decomposition import PCA
from sklearn.lda import LDA


def my_Decomposing(X,y,n):

#    X = iris.data
#    y = iris.target
#    target_names = iris.target_names
    
    
    pca = PCA(n_components=n)
    X_r = pca.fit(X).transform(X)
#    lda = LDA(n_components=n)
#    X_r2 = lda.fit(X, y).transform(X)    
    return X_r
    




def testTheModel(data,target):
    

    X_train, X_test, y_train, y_test = train_test_split(
        data, target, test_size=0.3, random_state=0)
     
    # Set the parameters by cross-validation
    tuned_parameters = [
                        {'n_estimators': [300,400,500], 'learning_rate': [0.1,0.05],
                         'subsample':[0.5],
                         'max_depth': [1,2,3],
#                         'max_features':[10,11],
                         'min_samples_leaf':[10,20,5,2],
#                        'loss':['ls','lad','huber','quantile'],
#                        'alpha':[0.1,0.3,0.5,0.7,0.9]

#                         'min_samples_split':[2,3]
                             }
                    
                         ]
    
    #############################################################################
    print "# Tuning hyper-parameters for "
    print 
    
    clf = GridSearchCV(GradientBoostingRegressor(loss='ls'), tuned_parameters, cv=5 )
    clf.fit(X_train, y_train)
    print  "Best scores:"
    print clf.best_score_    
    
    print "Best parameters set found on development set:"
    print 
    print clf.best_estimator_
    print 
#    print "Grid scores on development set:"
#    print 
#    for params, mean_score, scores in clf.grid_scores_:
#        print("%0.3f (+/-%0.03f) for %r"
#              % (mean_score, scores.std() / 2, params))
    print 
    
   
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print 
 



dataSet = np.random.permutation(BJ_DataSet) 
myData,myTarget=dataSet[:,1:-1],dataSet[:,-1]      

#n=15
#deX1 = my_Decomposing(myData,myTarget,n)
#testTheModel(deX1,myTarget)
    
    
testTheModel(myData,myTarget)   
    

    
    
    
    
    
    
    
    
    
    
    
    
    

