from scipy.io import loadmat
import numpy as np

ans = loadmat('ex8_movieParams.mat')
X = np.matrix(ans['X'])
Theta = np.matrix(ans['Theta'])
# num_users = int(ans['num_users'])
# num_movies = int(ans['num_movies'])
# num_features = int(ans['num_features'])
num_users = 4
num_movies = 5
num_features = 3
ans = loadmat('ex8_movies.mat')
Y = np.matrix(ans['Y'])
R = np.matrix(ans['R'])
print ans



X = X[0:num_movies, 0:num_features]
Theta = Theta[0:num_users, 0:num_features]
Y = Y[0:num_movies, 0:num_users]
R = R[0:num_movies, 0:num_users]
lambd = 1.5;

print 'X:'
print X
print 'Theta:'
print Theta
print 'Y:'
print Y
print 'R:'
print R
print 'X * Theta.conj().T'
print X * Theta.conj().T
print 'np.multiply(X * Theta.conj().T,R)'
print np.multiply(X * Theta.conj().T,R)
print 'np.multiply(X * Theta.T,R) - Y'
print np.multiply(X * Theta.T,R) - Y
print 'np.asarray(np.multiply(X * Theta.T,R) - Y)**2'
print np.asarray(np.multiply(X * Theta.T,R) - Y)**2
print 'np.sum(np.asarray(np.multiply(X * Theta.T,R) - Y)**2,axis = 1)'
print np.sum(np.asarray(np.multiply(X * Theta.T,R) - Y)**2,axis = 1)
print 'np.sum(np.sum(np.asarray(np.multiply(X * Theta.T,R) - Y)**2,axis = 1))'
print np.sum(np.sum(np.asarray(np.multiply(X * Theta.T,R) - Y)**2,axis = 1))
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
# J = cofiCostFunc([X(:) ; Theta(:)], Y, R, num_users, num_movies, num_features, 0);