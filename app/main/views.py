
from flask import render_template,request,redirect,url_for,abort
from . import main
from ..request import get_quotes
from flask_login import login_required,login_user,current_user
from ..models import  User,Blog,Quotes,Comment,Subscription
from .forms import UpdateProfile,BlogForm,CommentForm,SubscriptionForm,UpdateBlogForm
from .. import db,photos
from ..subscriber import mail_message


@main.route('/', methods = ['GET','POST'])
def index():

    blogs = Blog.query.all()
    quotes = get_quotes()
    form = SubscriptionForm()

    if form.validate_on_submit():
        email = form.email.data
        subscriber = Subcription(email = email)
        db.session.add(subscriber)
        db.session.commit()
        
        return redirect(url_for('main.index'))

       
    
    return render_template('index.html', quotes = quotes, blogs = blogs, form = form)


@main.route('/create_new',methods = ['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data      
        user_id = current_user
        new_blog_object = Blog(description = description,title =title,user_id=current_user._get_current_object().id)
        new_blog_object.save_blog()

        return redirect(url_for('main.index'))
    return render_template('blog.html',form=form)


@main.route('/comment/<int:blog_id>', methods = ['GET','POST'])
def comment(blog_id):
    form = CommentForm()
    blogs = Blog.query.get(blog_id)
    comments = Comment.query.filter_by(blog_id=blog_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        blog_id = blog_id
        new_comment = Comment(comment = comment,blog_id=blog_id)
        new_comment.save_comments()

        return redirect(url_for('.comment',blog_id = blog_id))

    return render_template('comment.html',form = form,blogs = blogs, comments = comments)


@main.route('/index/<int:id>/delete',methods = ['GET','POST'])
@login_required
def delete(id):
    current_post = Blog.query.filter_by(id = id).first()
    if current_post.user != current_user:
        abort(404)
    db.session.delete(current_post)
    db.session.commit()

    return redirect(url_for('.index'))


@main.route('/update/<int:id>',methods = ['GET','POST'])
@login_required
def update_blog(id):
    blogs = Blog.query.filter_by(id = id).first()
    if blogs is None:
        abort(404)
    form = UpdateBlogForm()
    if form.validate_on_submit():
        blogs.title = form.title.data
        blogs.description = form.description.data 
        db.session.add(blogs)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('update_blog.html',form = form)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))