import plotly.plotly as py
import plotly.graph_objs as go

from flask import Flask, render_template, request

from scipy.spatial.distance import pdist, squareform
from scipy.io import loadmat
from scipy.optimize import fmin_cg

# Local modules
from model.forms import SearchForm
from dao.movieDao import searchMovie

app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        print 'The form is received. '
        print form.name.data
        res = searchMovie(form.name.data)
        print 'returned'

        return render_template('result.html', search_res = res)
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

@app.route('/ratemovie/<int:movie_id>')
def rateMovie(movie_id):
    print 'the data has been received -- {0}'.format(movie_id)
    print 'loading ratings ...'
    pass

if __name__ == "__main__":
    app.run()