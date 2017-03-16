import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.io import loadmat

import plotly.plotly as py
import plotly.graph_objs as go


# Create the following array where each row is a point in 2D space:
# [[0 1]
#  [1 0]
#  [2 0]]
x = np.array([[1, 2, 3], [3, 4, 5], [5, 6, 7],[7, 8, 9]])
print 'The orginal array:\n'
print x.T
print '========='
print x.conj().T

# Compute the Euclidean distance between all rows of x.
# d[i, j] is the Euclidean distance between x[i, :] and x[j, :],
# and d is the following array:
# [[ 0.          1.41421356  2.23606798]
#  [ 1.41421356  0.          1.        ]
#  [ 2.23606798  1.          0.        ]]
d = squareform(pdist(x, 'euclidean'))
print 'The Euclidean distance between all rows of x\n'
print d

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


# data = [
#     go.Heatmap(z = Y)
# ]
# py.iplot(data, filename='basic-heatmap')
print R[0,] 
print Y[0, R[0,].ravel().nonzero()][1,]

print '%f /5 \n' % Y[0, R[0,].ravel().nonzero()][1,].mean()

print '=============================================================='

num_users = 4
num_movies = 5
num_features = 3
Theta = Theta[0:num_users, 0:num_features]
cofiCostFunc(vstack((X,Theta)))


def cofiCostFunc(params, Y ,R, num_users, num_movies, num_features, lambd):
	X = np.reshape(params[0,num_movies*num_features+1], (num_movies, num_features))
	print X
	pass
