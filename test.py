import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.io import loadmat

import plotly.plotly as py
import plotly.graph_objs as go


def cofiCostFunc(params, Y ,R, num_users, num_movies, num_features, lambd):
	print '=============== Here goes the cofiCostFunc =================='
	print num_movies*num_features
	print len(params[0, 0:num_movies*num_features+1])
	X = np.reshape(params[0, 0:num_movies*num_features], (num_movies, num_features))
	Theta = np.reshape(params[0, num_movies*num_features:], (num_users, num_features))
	print X
	print Theta
	print 'phase1'
	phase1 = (1./2) * np.sum(np.sum(np.asarray(np.multiply(X * Theta.T,R) - Y)**2,axis = 1))
	print phase1
	phase2 =  (lambd/float(2)) * np.sum(np.sum(np.asarray(Theta)**2,axis = 1)) 
	print 'phase2'
	print phase2
	phase3 = (lambd/float(2)) * np.sum(np.sum(np.asarray(X)**2,axis = 1))
	print phase3
	print 'all'
	print phase1 + phase2 + phase3
	pass

# Create the following array where each row is a point in 2D space:
# [[0 1]
#  [1 0]
#  [2 0]]
x = np.array([[1, 2, 3], [3, 4, 5], [5, 6, 7],[7, 8, 9]])
print 'The orginal array:\n'
print x.T
print '========='
print x.conj().T


print '==========================================================='

a = np.matrix([[1,2,3]])
b = np.matrix([[1],[2],[3]])
a = a.T
y = np.multiply(a,b)

print a.T
print b
print y


print 'Loading data:\n'
ans = loadmat('ex8_movies.mat')
Y = np.matrix(ans['Y'])
R = np.matrix(ans['R'])
print Y
print '\n'
print R
ans = loadmat('ex8_movieParams.mat')
X = np.matrix(ans['X'])
Theta = np.matrix(ans['Theta'])
num_users = int(ans['num_users'])
num_movies = int(ans['num_movies'])
num_features = int(ans['num_features'])

# data = [
#     go.Heatmap(z = Y)
# ]
# py.iplot(data, filename='basic-heatmap')

print R[0,] 
print Y[0, R[0,].ravel().nonzero()][1,]

print '%f /5 \n' % Y[0, R[0,].ravel().nonzero()][1,].mean()

print '=============================================================='

print X
print Theta
print X.flatten()
print Theta.flatten()

params = np.concatenate((X.flatten(),Theta.flatten()),axis = 1) 
print 'params len:'
print params[0,:]
cofiCostFunc(params=params, Y = Y ,R = R, num_users = num_users, num_movies = num_movies, num_features = num_features, lambd = 1.5)


