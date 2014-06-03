# -*- coding: utf-8 -*-
"""
Created on Wed May 14 15:58:05 2014

@author: zqh
"""

print(__doc__)

# Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
#
# License: BSD 3 clause
import matplotlib

import numpy as np
import pylab as pl
from sklearn import ensemble
#from sklearn import datasets
#from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error

###############################################################################
# Load data
#boston = datasets.load_boston()
#X, y = shuffle(boston.data, boston.target, random_state=13)
#X = X.astype(np.float32)
#offset = int(X.shape[0] * 0.9)
#X_train, y_train = X[:offset], y[:offset]
#X_test, y_test = X[offset:], y[offset:]



dataSet = np.random.permutation(BJ_DataSet) 

myData,myTarget=dataSet[:,1:-1],dataSet[:,-1]

selectedFetureName=SELECTED_FETURE_NAME[1:-1]
date = dataSet[:,0]
rat = 0.8
ratio = int(len(myData)*rat)

X_train, y_train = myData[:ratio], myTarget[:ratio]
X_test, y_test = myData[ratio:], myTarget[ratio:]





###############################################################################
# Fit regression model
params = {'n_estimators': 400, 'max_depth': 4, 'min_samples_split': 2,
          'subsample': 0.5,'min_samples_leaf': 2,
          'learning_rate': 0.01, 'loss': 'ls'}
          
          
          
clf = ensemble.GradientBoostingRegressor(**params)


clf.fit(X_train, y_train)
y_predict = clf.predict(X_test)
error = y_predict-y_test

pl.scatter(date[ratio:],error)
pl.show()


print clf.score(X_test, y_test)
mse = mean_squared_error(y_test, clf.predict(X_test))
print("MSE: %.4f" % mse)

###############################################################################
# Plot training deviance
myFonts=matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simhei.ttf')

# compute test set deviance
test_score = np.zeros((params['n_estimators'],), dtype=np.float64)

for i, y_pred in enumerate(clf.staged_decision_function(X_test)):
    test_score[i] = clf.loss_(y_test, y_pred)

#pl.figure(figsize=(12, 6))
#pl.subplot(1, 2, 1)


pl.title('Deviance')
pl.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-',
        label='Training Set Deviance')
pl.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
        label='Test Set Deviance')
pl.legend(loc='upper right')
pl.xlabel('Boosting Iterations')
pl.ylabel('Deviance')
pl.show()
###############################################################################
# Plot feature importance
feature_importance = clf.feature_importances_
# make importances relative to max importance
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + .5

#pl.subplot(1, 2, 2)

pl.barh(pos, feature_importance[sorted_idx], align='center')

pl.yticks(pos, selectedFetureName[sorted_idx],fontproperties=myFonts)
pl.xlabel('Relative Importance')
pl.title('Variable Importance')
pl.show()

