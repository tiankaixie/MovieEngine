import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.io import loadmat
from scipy.optimize import fmin_cg

import plotly.plotly as py
import plotly.graph_objs as go

def normalizeRatings(Y, R):
	print Y.shape
	[m,n] = Y.shape
	print m
	print n
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
	print phase1 + phase2 + phase3

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

def loadMovie():
	bucket = []
	file = open('movie_ids.txt', 'r')
	for line in file:
		info = line.split(' ',1)
		bucket.append(info[1][:-1])
	print bucket
	return bucket


# =============================================================
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

print '%f /5 \n' % Y[0, R[0,].ravel().nonzero()][1,].mean()

params = np.concatenate((X.flatten(),Theta.flatten()),axis = 1) 

cofiCostFunc(params=params, Y = Y ,R = R, num_users = num_users, num_movies = num_movies, num_features = num_features, lambd = 1.5)

print 'now we are going to implemente the minimize fuction.. hopefully in will work\n'


print X.shape
print Theta.shape

print 'Now for new users to rate the movie:'

my_ratings = np.matlib.zeros((1682,1))

my_ratings[0] = 4
my_ratings[97] = 2
my_ratings[6] = 3
my_ratings[11] = 5
my_ratings[53] = 4
my_ratings[63] = 5
my_ratings[65] = 3
my_ratings[68] = 5
my_ratings[182] = 4
my_ratings[225] = 5
my_ratings[354] = 5

movieList = loadMovie()
print movieList[0]
print movieList[97]
print movieList[6]
print movieList[11]
print movieList[53]
print movieList[63]
print movieList[65]
print movieList[68]
print movieList[182]
print movieList[225]
print movieList[354]

print 'combine my ratings with matrix'
print Y.shape
Y = np.concatenate((my_ratings,Y),1)
#print Y.shape
idx = my_ratings.ravel().nonzero()
idx = idx[1]
my_mask = np.matlib.zeros((1682,1))
my_mask[idx] = 1
#print R.shape
R = np.concatenate((my_mask,R),1)
#print R.shape
[Ynorm, Ymean] = normalizeRatings(Y, R)
[num_movies , num_users] = Y.shape
num_features = 10;
print num_users
print num_movies

X = np.matlib.randn(num_movies,num_features)
Theta = np.matlib.randn(num_users,num_features)

initial_parameters = np.concatenate((X.flatten(),Theta.flatten()),axis = 1) 
print 'executing'

print initial_parameters.shape
res= fmin_cg(f = cofiCostFunc, x0 = initial_parameters ,fprime = compute_grad, args = (Ynorm ,R , num_users, num_movies, num_features, 10), maxiter = 100,disp = True)

# print res.shape
# , fopt, fun_calls, grad_calls, warnflag, allevcs 

X = np.reshape(res[0:num_movies*num_features], (num_movies, num_features))
Theta = np.reshape(res[num_movies*num_features:], (num_users, num_features))
print X.shape
print Theta.shape

predict = np.matrix(X)*np.matrix(Theta).T;
print 'predict'
print predict.shape
print Ymean.shape
my_predict = predict[:,0] + Ymean

print my_predict
n = len(my_predict)
ranks = sorted(range(len(my_predict)), key = my_predict.__getitem__ , reverse = True)
print my_predict[ranks]
movielist = np.array(movieList)[ranks]
print movielist
for x in xrange(0,10):
	print '[{0}] : {1} '.format(x,movielist[x])
