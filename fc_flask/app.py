import os
from flask import Flask
from flask import render_template
from flask import request, redirect, session
from models import db
from models import Fcuser
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

app = Flask(__name__)

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/')

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        session['userid'] = form.data.get('userid')
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

    # if request.method =='POST':
    #     userid = request.form.get('userid')
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     re_password = request.form.get('re-password')

    #     if (userid and username and password and re_password) and (password == re_password):

            fcuser = Fcuser()
            fcuser.userid = form.data.get('userid')
            fcuser.username =  form.data.get('username')
            fcuser.password =  form.data.get('password')
            
            db.session.add(fcuser)
            db.session.commit()
            return redirect('/')
    return render_template('register.html',form=form)

@app.route('/')
def hello_world():
    userid = session.get('userid', None)
    return render_template('hello.html', userid = userid) #"Hello World"

basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'qasdzxcgqQ'

csrf = CSRFProtect()
csrf.init_app(app)

db.init_app(app)
db.app = app
db.create_all()

if __name__== "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)