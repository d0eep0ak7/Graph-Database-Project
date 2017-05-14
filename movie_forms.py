from flask import Flask, request, redirect, url_for, render_template, flash,session
from flask import Blueprint
import json
import math
import requests
from movie_models import genres_list,rate_movie,rated_movie,similar_movies,suggest_movies

movie_app= Blueprint('movie_app', __name__)



@movie_app.route('/movie', methods=['GET','POST'])
def movie():
    imdbid=request.form['imdbid']
    r = requests.get('http://www.omdbapi.com/?i='+imdbid)
    data = json.loads(r.text)
    source=data['Poster']
    return render_template("main.html",source=source)


@movie_app.route('/genres/<genre_name>/<int:skip>/<int:page>', methods=['GET','POST'])
def genres(genre_name,skip,page):




    results,resultscount=genres_list(genre_name,102,skip)
    pagenumbers = math.ceil(resultscount / 102)
    return render_template("/movies/genres.html",genre_name=genre_name,results=results,resultscount=resultscount,pagenumbers=pagenumbers,skip=skip,page=page)

@movie_app.route('/ratemovies', methods=['GET','POST'])
def ratemovies():
    imdbId = request.json['imdbId']
    stars= request.json['stars']
    print(imdbId)
    print(stars)
    username=session['username']
    rate_movie(username,imdbId,stars)

    return 'OK'


@movie_app.route('/ratedmovies/<int:skip>/<int:page>', methods=['GET','POST'])
def ratedmovies(skip,page):
    username = session['username']
    results, resultscount =rated_movie(username,skip)

    pagenumbers=math.ceil(resultscount/102)


    return render_template("/movies/rated_movies.html", results=results, resultscount=resultscount,pagenumbers=pagenumbers,skip=skip, page=page)


@movie_app.route('/similarmovies/')
def similarmovies():
    username = session['username']
    results=similar_movies(username)
    return render_template("/movies/similar_movies.html", results=results)

@movie_app.route('/suggestedmovies/')
@movie_app.route('/suggestmovies/')
def suggestmovies():

    results=""
    return render_template("/movies/suggest_movies.html", results=results)



@movie_app.route('/suggestedmovies/', methods=['POST'])
def suggestedmovies():
    username = session['username']
    gender = request.form['gender']
    criteria=request.form['selection']
    companion= request.form['companion']
    emotions = request.form['emotions']


    if companion=='not_specified' or emotions=='not_specified' or  criteria=='not_specified':
        flash('Please specify all the fields')
        return redirect(request.referrer)
    results1=suggest_movies(username,gender,companion,emotions,criteria)


    return render_template("movies/suggested_movies.html", results1=results1)