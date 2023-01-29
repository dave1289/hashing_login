from flask import Flask, redirect, render_template, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, bcrypt, Tweet
from forms import UserForm, TweetForm

app = Flask(__name__)

# standardized sqlalchemy init setting and variable structure
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_hash'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False
app.config['SECRET_KEY'] = '2333'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)
# app.debug = True

app.app_context().push()

connect_db(app)

@app.route('/')
def show_home():
   return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def registration():
   form = UserForm()
   if form.is_submitted():
      username = form.username.data
      password = form.password.data
      if not User.query.filter_by(username=username).first():
         new_user = User.register(username, password)
         db.session.add(new_user)
         db.session.commit()
         session['user_id'] = new_user.user_id
         flash('Welcome! Successfully created your account!', 'success')
         return redirect('/tweets')
      else:
         form.username.errors = ['Username taken']
   return render_template('register.html', form=form)

@app.route('/tweets', methods=['GET', 'POST'])
def show_tweets():
   form = TweetForm()
   tweets = Tweet.query.all()
   if "user_id" not in session:
      flash('Please login to see tweets', 'error')
      return redirect('/login')
   else:
      if form.is_submitted():
         comment = form.comment.data
         user = session['user_id']
         new_comment = Tweet(user_id = user, comment=comment)
         db.session.add(new_comment)
         db.session.commit()
         return redirect('/tweets')
      else:
         return render_template('tweets.html', form=form, tweets=tweets)


@app.route('/tweets/<int:id>', methods=["POST"])
def delete_tweet(id):
   """delete tweet"""
   if 'user_id' not in session:
      flash("Please login first!", 'error')
      return redirect('/tweets')
   tweet = Tweet.query.get_or_404(id)
   if tweet.user_id == session['user_id']:
      db.session.delete(tweet)
      db.session.commit()
      flash('You have deleted your tweet', 'info')
      return redirect('/tweets')
   else:
      flash('You are not authorized to delete this tweet.', 'error')
      return redirect('/tweets')

   
@app.route('/login', methods=["GET", "POST"])
def login_user():
   form = UserForm()
   if form.is_submitted():
      username = form.username.data
      password = form.password.data
      user = User.authenticate(username, password)
      if user:
         flash(f'Welcome back, {user.username}', 'success')
         session['user_id'] = user.user_id
         return redirect('/tweets')
      else:
         form.username.errors = ['Invalid username/password']
   return render_template('login.html', form=form)

@app.route('/logout')
def logout():
   user = User.query.get(session['user_id'])
   flash(f'Goodbye, {user.username} come again soon!', 'success')
   session.pop('user_id')
   return redirect('/')

