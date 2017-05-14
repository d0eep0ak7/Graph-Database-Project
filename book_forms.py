from flask import Flask, request, redirect, url_for, render_template, flash,session
from flask import Blueprint

from book_models import listmovie ,book_status,book_recommendations,my_books,my_books_to_read
book_app= Blueprint('book_app', __name__)



@book_app.route('/bookmain/<search_id>', methods=['GET','POST'])
def bookmain(search_id):
       results=listmovie(search_id)




       return render_template("/books/book_main.html",results=results)



@book_app.route('/bookstatus', methods=['GET','POST'])
def bookstatus():
    isbn= request.json['isbn']
    status= request.json['status']
    print(isbn)
    print(status)
    username=session['username']

    book_status(username,isbn,status)

    return 'OK'


@book_app.route('/bookrecommendations/')
def bookrecommendations():
       username = session['username']


       results=book_recommendations(username)


       return render_template("/books/book_recommendations.html",results=results)


@book_app.route('/mybooks/')
def mybooks():
       username = session['username']


       result1=my_books(username)


       return render_template("/books/my_books.html",result1=result1)


@book_app.route('/mybookstoread/')
def mybookstoread():
       username = session['username']


       result2=my_books_to_read(username)


       return render_template("/books/mybookstoread.html",result2=result2)