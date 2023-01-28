from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
   db.app = app
   db.init_app(app)

class User(db.Model):
   """table of users for demo hash"""
   __tablename__ = 'users'

   def __repr__(self):
      s = self
      return f'<USER user_id:{s.user_id} username:{s.username} password:{s.password}'

   user_id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String, nullable=False, unique=True)
   password = db.Column(db.String, nullable=False)

   @classmethod
   def register(cls, username, pwd):

      hashed = bcrypt.generate_password_hash(pwd)
      # turn bytestring to unicode 8
      hashed_utf8 = hashed.decode("utf8")

      return cls(username=username, password=hashed_utf8)

   @classmethod
   def authenticate(cls, username, pwd):
      # authenticates user credentials and keeps them logged in
      u = User.query.filter_by(username=username).first()

      if u and bcrypt.check_password_hash(u.password, pwd):
         # checks input password to DB hashed password entry
         return u
      else:
         return False


class Tweet(db.Model):
   """table for tweets by users"""
   __tablename__ ='tweets'

   def __repr__(self):
      s = self
      return f'<TWEET Comment_id:{s.id} User_id:{s.user_id} Comment={s.comment}>'

   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
   comment = db.Column(db.String(120), nullable=False)

   user = db.relationship('User', backref="tweets")