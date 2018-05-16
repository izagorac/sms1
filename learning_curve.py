# File:        learning_curve.py
#
# Author:      Rohan Patel
#
# Date:        05/16/2018
#
# Description:

import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def learning_curve(tfidf_vect, messages, folds):
	training_set_size = []
	train_error = []
	cv_error = []

	print("")
	print("This may take some time, please wait..", sep=' ', end='', flush=True)
	for training_size in range(10, len(messages), 75):
		print(".", sep=' ', end='', flush=True)
		X = tfidf_vect[:training_size]
		y = messages['label'][:training_size]
		kf = KFold(n_splits=folds, random_state=None, shuffle=False)
		err1 = []
		err2 = []

		# generate K folds and train classifier on every fold
		for train_index, test_index in kf.split(X):
			#print("TRAIN:", train_index, "TEST:", test_index)
			X_train, X_test = X[train_index], X[test_index]
			y_train, y_test = y[train_index], y[test_index]

			svm = SVC(C = 100, gamma = 0.01)
			svm.fit(X_train, y_train)
			pred = svm.predict(X_test)

			err = 1.0 - (svm.score(X_train,y_train))
			err1.append(err) # training error
			err = 1.0 - (svm.score(X_test,y_test))
			err2.append(err) # cv error

		train_error.append(np.average(err1)) # training error =  avg of training error from every fold
		cv_error.append(np.average(err2))    # cross-validation error = avg of cv error from every fold
		training_set_size.append(training_size)

	# Plotting of learning curve using matplotlib
	x = training_set_size
	y = train_error
	z = cv_error

	fig = plt.figure(figsize=(13,8))
	plt.plot(x,y, label='Training error')
	plt.plot(x,z,'g-', label='Cross-Validation error')
	plt.xlabel('Training Set Size')
	plt.ylabel('Error Rate')
	plt.title('Learning Curve')
	plt.legend()
	plt.show(block = True)

def main():

	tfidf_vect = pickle.load(open("output/tfidf_vector.pickle", "rb"))
	messages = pd.read_csv('output/processed_msgs.csv')

	learning_curve(tfidf_vect, messages, folds = 5)
	#learning_curve(tfidf_vect, messages, folds = 10)

if __name__ == "__main__":
    main()