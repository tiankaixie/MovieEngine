from flask import Flask
from flask import render_template
from flask import request
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.io import loadmat
from scipy.optimize import fmin_cg

import plotly.plotly as py
import plotly.graph_objs as go
import re
from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email Address', [validators.Length(min=6, max=35)])
	password = PasswordField('New Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords must match')
		])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class SearchForm(Form):
    name = StringField('Moviename')

def loadMovie():
    bucket = []
    file = open('movie_ids.txt', 'r')
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
    return movieList[res_idx]


app = Flask(__name__)



@app.route('/',methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        print 'The form is received. '
        print form.name.data
        search_res = searchMovie(form.name.data)
        print 'returned'
        return render_template('result.html', search_res = search_res)
    return render_template('search.html', form = form)


@app.route('/searchById/<int:movie_id>')
def searchById(movie_id):
    return '%d \n' % movie_id


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run()