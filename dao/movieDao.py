import re
import numpy as np

data_movies = loadmat('data/ex8_movies.mat')
data_movies_params = loadmat('data/ex8_movieParams.mat')

def loadMovie():
    bucket = []
    file = open('data/movie_ids.txt', 'r')
    for line in file:
        info = line.split(' ',1)
        bucket.append(info[1][:-1])
    # print bucket
    return bucket

def searchMovie(movieName):
    print 'enter search:'
    movieList = loadMovie()
    res_idx = [i for i, movie in enumerate(movieList) if re.search(movieName, movie, re.I)]
    print res_idx
    movieList = np.asarray(movieList)
    print 'going to return'
    res = zip(res_idx, movieList[res_idx])
    return res

def loadData():
    print 'Loading data:\n'
    Y = np.matrix(data_movies['Y'])
    R = np.matrix(data_movies['R'])
    X = np.matrix(data_movies_params['X'])
    Theta = np.matrix(data_movies_params['Theta'])
    num_users = int(data_movies_params['num_users'])
    num_movies = int(data_movies_params['num_movies'])
    num_features = int(data_movies_params['num_features'])
    return Y, R, X, Theta, num_users, num_movies, num_features