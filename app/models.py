from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quotes:

    def __init__(self,id,author,quote,permalink):
        self.id = id
        self.author = author
        self.quote = quote
        self.permalink = "http://quotes.stormconsultancy.co.uk/quotes/31"


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
 

    blogs = db.relationship('Blog', backref='user',  lazy="dynamic")
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)
    

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(500))
    title = db.Column(db.String(255))     

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable = False)
    comments = db.relationship('Comment', backref='blogs', lazy='dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    
    @classmethod
    def clear_blog(cls):
        Bloc.blog.clear()

    @classmethod
    def get_blogs(cls):
        blog = Blog.query.filter_by(id = id).all()
        return blog


    def __repr__(self):
        return f'Blog{self.description}' 




class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.Text())

    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)

    def save_comments(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_comment(self):
        Comment.comments.clear()

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(blog_id = id).all()
        return comments    

    def __repr__(self):
        return f"Comment{self.comment}"

class Subscription(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(255), unique = True, index = True)


    def save_sub(self):
        db.session.add(self)
        db.session.commit(self)

    def __repr__(self):
        return f'Subscription{self.email}'