import plotly.plotly as py
import plotly.graph_objs as go

from flask import Flask, render_template, request

from scipy.spatial.distance import pdist, squareform
from scipy.optimize import fmin_cg

# Local modules
from model.forms import SearchForm
from dao.movieDao import searchMovie
from utils.learning import collaborateFiltering

app = Flask(__name__, static_url_path='/static')


@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print 'The form is received. '
        print request.form.get('movieName')
        res = searchMovie(request.form.get('movieName'))
        print 'returned'

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

@app.route('/ratemovie/<int:movie_id>')
def rateMovie(movie_id):
    print 'the data has been received -- {0}'.format(movie_id)
    print 'loading ratings ...'
    pass

@app.route('/getrecommend')
def getRecommend():
    res = collaborateFiltering()
    return render_template('recommendation.html', movies = res)
    
    

if __name__ == "__main__":
    app.run()