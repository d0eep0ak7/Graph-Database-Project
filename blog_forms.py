from flask import Flask, request, redirect, url_for, render_template, flash,session
from flask import Blueprint
from models import register,verify_user
from blog_models import addpost,like_post,get_todays_recent_posts,get_recent_posts,get_similar_users,get_commonality_of_user,delete_post
blog_app= Blueprint('blog_app', __name__)

@blog_app.route('/add_post', methods=['GET','POST'])
def add_post():





    try:

        username=session['username']
        title = request.form['title']
        tags = request.form['tags']
        text = request.form['text']
        about= request.form['about']
        print(about)
        print(tags)
        print(text)
        print(about)

        print(title)
        if not title:
            flash('You must give your post a title.')
        elif not tags:
            flash('You must give your post at least one tag.')
        elif not about:
            flash('You must give your post a text body.')

        elif not text:
            flash('You must give your post a text body.')
        else:
            addpost(username,title, tags, text,about)
            flash("Posted Successfully")
    except Exception as e:
        print("Hahaha")
    else:
        return redirect(url_for('blogmain'))



@blog_app.route('/likepost/<post_id>', methods=['GET','POST'])
def likepost(post_id):
    username = session.get('username')

    if not username:
        flash('You must be logged in to like a post.')
        return redirect(url_for('login'))

    like_post(username,post_id)

    flash('Liked post.')
    return redirect(request.referrer)





@blog_app.route('/deletepost/<post_id>')
def deletepost(post_id):
    username = session.get('username')

    if not username:
        flash('You must be logged in to delete a post.')
        return redirect(url_for('login'))

    cursor=delete_post(username,post_id)
    if cursor:


        flash('Post Deleted')
    else:
        flash('Post not deleted')
    return redirect(request.referrer)








@blog_app.route('/profile/<username>')
def profile(username):
    logged_in_username = session.get('username')
    user_being_viewed_username = username


    posts = get_recent_posts(user_being_viewed_username)

    similar = []
    common = []

    if logged_in_username:


        if logged_in_username ==  user_being_viewed_username:
            similar = get_similar_users(logged_in_username)
        else:
            common = get_commonality_of_user(logged_in_username,user_being_viewed_username)

    return render_template('/blog/profile.html',
        username=username,
        posts=posts,
        similar=similar,
        common=common
    )



