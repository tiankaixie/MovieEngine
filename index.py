import plotly.plotly as py
import plotly.graph_objs as go

from flask import Flask, render_template, request, session

from scipy.spatial.distance import pdist, squareform
from scipy.optimize import fmin_cg
from flask import json

# Local modules
from model.forms import SearchForm
from dao.movieDao import searchMovie, getMyRatings
from utils.learning import collaborateFiltering

app = Flask(__name__, static_url_path='/static')
app.secret_key = "super secret key"


@app.route('/',methods=['GET', 'POST'])
def index():
    if 'user_rate' not in session:
        my_ratings = getMyRatings()
        session['user_rate'] = my_ratings.tolist()
    if request.method == 'POST':
        print 'The form is received. '
        print request.form.get('movieName')
        res = searchMovie(request.form.get('movieName'))
        print 'returned'
        print res
        return render_template('result.html', search_res = res)
    return render_template('search.html')

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

@app.route('/info/<int:movie_id>')
def movieInfo(movie_id):
    if 'user_rate' not in session:
        my_ratings = getMyRatings()
        session['user_rate'] = my_ratings
    else:
        my_ratings = session['user_rate']
    print 'the data has been received -- {0}'.format(movie_id)
    print 'ratings:'
    print my_ratings[movie_id]
    return render_template('details.html',score = my_ratings[movie_id], movie_id = movie_id)

@app.route('/info/rateMovie/<int:movie_id>', methods = ['GET','POST'])
def rateMovie(movie_id):

    print 'the data has been received -- {0}'.format(movie_id)
    print 'loading ratings ...'
    if request.method == 'POST':
        pass
    if 'user_rate' not in session:
        my_ratings = getMyRatings()
        session['user_rate'] = my_ratings
    else:
        my_ratings = session['user_rate']
    my_ratings[movie_id] = request.form.get('score')
    print my_ratings[movie_id]
    session['user_rate'] = my_ratings
    print 'finished.'
    pass

@app.route('/getrecommend')
def getRecommend():
    res = collaborateFiltering()
    return render_template('recommendation.html', movies = res)
    
    

if __name__ == "__main__":
    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app)
    # app.debug = True
    app.run()