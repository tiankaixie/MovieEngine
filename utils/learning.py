import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.io import loadmat
from scipy.optimize import fmin_cg

import plotly.plotly as py
import plotly.graph_objs as go

from dao.movieDao import loadData, loadMovie

def normalizeRatings(Y, R):
	[m,n] = Y.shape
	Ymean = np.matlib.zeros((m, 1))
	Ynorm = np.matlib.zeros((m, n))
	for i in range(m):
		idx = R[i,].ravel().nonzero()
		#print idx[1]
		idx = idx[1]
		Ymean[i] = Y[i, idx].mean()
		#print Ynorm
		Ynorm[i, idx] = Y[i, idx] -  Ymean[i]
	return Ynorm, Ymean

def cofiCostFunc(params, Y ,R, num_users, num_movies, num_features, lambd):
	params = np.matrix(params)
	# print len(params[0, 0:num_movies*num_features+1])
	X = np.reshape(params[0,0:num_movies*num_features], (num_movies, num_features))
	Theta = np.reshape(params[0,num_movies*num_features:], (num_users, num_features))
	phase1 = (1./2) * np.sum(np.sum(np.asarray(np.multiply(X * Theta.T,R) - Y)**2,axis = 1))
	phase2 =  (lambd/float(2)) * np.sum(np.sum(np.asarray(Theta)**2,axis = 1)) 
	phase3 = (lambd/float(2)) * np.sum(np.sum(np.asarray(X)**2,axis = 1))
	# print phase1 + phase2 + phase3
	return phase1 + phase2 + phase3

def compute_grad(params, Y ,R, num_users, num_movies, num_features, lambd):
	params = np.matrix(params)
	# print len(params[0, 0:num_movies*num_features+1])
	X = np.reshape(params[0,0:num_movies*num_features], (num_movies, num_features))
	Theta = np.reshape(params[0,num_movies*num_features:], (num_users, num_features))
	X_grad = (np.multiply(X * Theta.T, R) - Y)*Theta + lambd * X
	
	Theta_grad = (np.multiply(X * Theta.T, R) - Y).T * X + lambd * Theta
	grad = np.concatenate((X_grad.flatten(),Theta_grad.flatten()),axis = 1)
	return np.squeeze(np.asarray(grad))

def collaborateFiltering():
	# this data could be loaded from dao, which is to say 
	# it could be gotten from the database instead of being 
	# from the mat file. Aslo, the ratings from user should 
	# be in the database so that when learning we are trying
	# to get them
	# Y is a 1682x943 matrix, containing ratings (1-5) of 
	# 1682 movies on 943 users
	# R is a 1682x943 matrix, where R(i,j) = 1 if and only 
	# if user j gave a rating to movie i

	[Y, R, X, Theta, num_users, num_movies, num_features] = loadData()
	[Ynorm, Ymean] = normalizeRatings(Y, R)
	[num_movies , num_users] = Y.shape
	num_features = 10;
	X = np.matlib.randn(num_movies,num_features)
	Theta = np.matlib.randn(num_users,num_features)
	initial_parameters = np.concatenate((X.flatten(),Theta.flatten()),axis = 1) 
	print 'executing the learning algorithm...'
	print initial_parameters.shape

	res= fmin_cg(f = cofiCostFunc, x0 = initial_parameters ,fprime = compute_grad, args = (Ynorm ,R , num_users, num_movies, num_features, 10), maxiter = 100,disp = True)
	# print res.shape
	# , fopt, fun_calls, grad_calls, warnflag, allevcs 
	X = np.reshape(res[0:num_movies*num_features], (num_movies, num_features))
	Theta = np.reshape(res[num_movies*num_features:], (num_users, num_features))

	predict = np.matrix(X)*np.matrix(Theta).T;
	print 'predicting:'
	my_predict = predict[:,0] + Ymean

	n = len(my_predict)
	ranks = sorted(range(len(my_predict)), key = my_predict.__getitem__ , reverse = True)
	# print my_predict[ranks]
	movieList = loadMovie()
	movielist = np.array(movieList)[ranks]
	print movielist
	for x in xrange(0,10):
		print '[{0}] : {1} '.format(x,movielist[x])
	return movielist[0:10]