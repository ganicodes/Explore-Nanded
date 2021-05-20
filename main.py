from flask import Flask, render_template, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime

with open('config.json', 'r') as c:
    parameters= json.load(c)['parameters']
local_server = True

app = Flask(__name__)
app.secret_key = 'SECRET KEY'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=parameters['gmail-user'],
    MAIL_PASSWORD=parameters['gmail-password']
)
mail = Mail(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/explorenanded'
db = SQLAlchemy(app)


class Contact(db.Model):
    '''sno, name, email,phone_  num, msg, date'''

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    phone_num = db.Column(db.String(80), unique=False, primary_key=True)
    msg = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.String(80), unique=False, nullable=True)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/history")
def history():
    return render_template('history.html')


@app.route("/gurudwara")
def gurudwara():
    return render_template('gurudwara.html')


@app.route("/touristguide")
def need_guide():
    return render_template('touristguide.html')


@app.route("/rentacar")
def need_car():
    return render_template('rentacar.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if 'user' in session or session==parameters['admin_user']:
        data=Contact.query.all()
        return render_template('dashboard.html',parameters=parameters,contacts=data)

    if request.method=='POST':
        user_name=request.form.get('username')
        user_password=request.form.get('password')
        if user_name==parameters['admin_user'] and user_password==parameters['admin_password']:
            session['user']=user_name
            data = Contact.query.all()
            return render_template('dashboard.html', parameters=parameters, contacts=data)

    return render_template('login.html',parameters=parameters)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        # leftside=databasevariable
        entry = Contact(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        print ("Your request for contact has been submitted successfully")
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients=[parameters['gmail-user']],
                          body=message + "\n" + phone)
        return render_template('index.html')

    return render_template('contact.html')


@app.route("/logout")
def logout():
    session.pop('user')
    return render_template('index.html')

@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/post")
def post():
    return render_template('post.html')


app.run(debug=True)

