from flask import Flask, render_template
from flask import Flask, request, session, redirect, url_for, render_template, flash
from functools import wraps
from forms  import forms_app
from blog_forms import blog_app
from movie_forms import movie_app
from book_forms import book_app
from datetime import datetime
import json
import requests
from blog_models import get_todays_recent_posts,get_similar_users
from movie_models import random_movies,update_similarity
app = Flask(__name__)
app.register_blueprint(forms_app)
app.register_blueprint(blog_app)
app.register_blueprint(movie_app)
app.register_blueprint(book_app)
app.secret_key = 'deepak'



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)

        else:
            flash("You need to login first")



            return render_template("homepage.html")

    return wrap



def already_loggedin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return render_template("main.html")
        else:
            return render_template("homepage.html")
    return wrap





@app.route('/')
@already_loggedin
def hello_world():
    return render_template("homepage.html")


@app.route('/main.html/')

@login_required

def main():
    return render_template("main.html")












@app.route('/blankpage')

@login_required

def blankpage():
    return render_template("blank-page.html")








@app.route('/blogmain.html/')

@login_required

def blogmain():

    posts = get_todays_recent_posts()



    return render_template("/blog/blogmain.html",posts=posts)








@app.route('/moviemain.html/')

@login_required

def moviemain():



    return render_template("/movies/movie_main.html")





@app.route('/trymovies.html/')

@login_required

def trymovies():

    username=session['username']
    results=random_movies(username)

    return render_template("/movies/try_movies.html",results=results)















@app.route('/similar_users')

@login_required

def similar_users():
    loggedin_user=session['username']
    similar = get_similar_users(loggedin_user)





    return render_template("/blog/similar_users.html",similar=similar)














@app.route('/signupModal.html/')

def signUp():
    return render_template("signupModal.html")


@app.route('/charts')
def charts():
    return render_template("charts.html")



@app.route('/forms.html/')
def forms():
    return render_template("charts.html")

@app.route('/signupError.html/')
def signupError():
    return render_template("signupError.html")

@app.route('/bootstrap-elements.html/')
def elements():
    return render_template("bootstrap-elements.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")

    return render_template("homepage.html")





def getimage(imdbid):
    print(imdbid)
    r = requests.get('http://www.omdbapi.com/?i=' + imdbid)
    data = json.loads(r.text)

    try:
        source = data['Poster']
    except KeyError:
        print("Key 2 is not exist!")
        source="Image Not Available"

    return source

app.jinja_env.globals.update(getimage=getimage)


def getpostime(timeinseconds):
    str=''
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    currenttime = delta.total_seconds()

    s = int(currenttime - timeinseconds)
    print(int(s/3600))
    if s <= 1:
        str='just now'
    elif s < 60:

        str = '{} seconds ago'.format(s)

    elif s < 120:
        str='1 minute ago'
    elif s < 3600:
        str = '{} minutes ago'.format(int(s / 60))
    elif s < 7200:
       str='1 hour ago'
    elif  s < 86400:
        str = '{} hours ago'.format(int(s / 3600))
    elif s < 604800:
        str = '{} day(s) ago'.format(int(s / 86400))
    else:
        str='on printdate'
    return str

app.jinja_env.globals.update(getpostime=getpostime)



def updatesimiliraties():

    update_similarity()
    return "Movies Database being Updated ...."


app.jinja_env.globals.update(updatesimiliraties=updatesimiliraties)

if __name__ == '__main__':
    app.run(debug=True)

