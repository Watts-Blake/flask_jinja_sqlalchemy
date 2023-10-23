# Lets Create a Project

## What Were doing

In this lecture we will create a project with flask as our api framework, along with sqlite3 and using jinja/wtf for server side rendering

## What we need to do

- Create a flask server
- Connect that server to our database
- Create Routes and templates on our server to render
  - GET - All Patients
  - GET - One Patient by id
  - GET - Form for creating a patient
  - POST - A new patient
- move all patients routes to a blue print and connect it to our app
- Create a nav bar and extend to it on all of our templates

<br/>

## 1). Create our Flask application

### In Terminal Run

```
mkdir app
cd app
touch __init__.py
```

###

## Install Dependencies

```
pipenv install Flask~=1.1
pipenv install Jinja2~=2.11
pipenv install python-dotenv~=0.13
pipenv install Flask-WTF~=0.14
pipenv install markupsafe==2.0.1
```

### Create Your Flask App in init of App dir

```
from flask import Flask

# initiate your app __name__ uses curr module
app = Flask(__name__)
```

### Setup up you flask ENV [Flask Config Docs](https://flask.palletsprojects.com/en/1.1.x/config/)

This file sets publicly visible environment variables for your Flask app

- in terminal run and root dir of proj not app

```
touch .flaskenv
```

- in .flaskenv add flask variables

```
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=true

# FLASK_ENV will default to production if not set.

# Setting FLASK_ENV to development will enable flasks builtin debugger tools that will log more information for you.

# FLASK_DEBUG=true will restart your server on any changes to your init py
```

### Configuring our flask app with a class

- create a new file called config.py in your app dir

```
import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
```

- navigate to your app dir init file then import your config file and add this under your creation of app

```
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
```

### Create a route on **init**.py [Route Decorator Docs](<https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.route:~:text=in%20the%20package.-,route(rule%2C%20**options),-%C2%B6>)

```
# we can create a route using the @ to use flasks bultin decorators while including the path

@app.route('/')

# create your function for that decorated route
def index():
    # do the thing, return what you want to return
    return 'We Made Our First Flask Route!!!'
```

### Create a jinja template for our index

- create a template dir in our app dir
- create a file named index.html
- write html to for our index template

```
<html>
  <head>
    <title>{{ page }} - {{ sitename }}</title>
  </head>

  <body>
    <h1>{{ sitename }}</h1>
    <h2>{{ page }}</h2>
    <p>Coming soon to a browser near you...</p>
  </body>
</html>
```

render this template under our / route

```
from flask import (Flask, render_template)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', sitename='Patient Tracker', page='Home')

```

<br/>

## 2). Setup and Connect Our Database

### Setup

- Create and open a database file

in terminal run

```
sqlite3 dev.db
```

- Create our patients
  run this command in sqlite3 shell

```
DROP TABLE patients IF EXISTS;
CREATE TABLE patients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL
);
INSERT INTO patients (first_name, last_name, email)
VALUES
('Tim', 'Petrol', 'rotary@fast.com'),
('Ryan', 'Runner', '10sec@jdm.com'),
('Tia', 'Petrol', 'typer@wtec.com');
```

### Connect

on your init py of your app add this code

```
import sqlite3

DB_FILE = "../dev.db"

with sqlite3.connect(DB_FILE) as conn:
    print(conn)
```

anywhere that we want to connect with our sqlite3 db will will need to import and use this to connect

### Reset, Reseed DB every time app is started

```
with sqlite3.connect(DB_FILE) as conn:
    curs = conn.cursor()
    curs.execute("DROP TABLE IF EXISTS patients;")
    curs.execute(
        """
        CREATE TABLE patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
        );
        """)
    curs.execute(
        """
        INSERT INTO patients (first_name, last_name, email)
        VALUES
        ('Tim', 'Petrol', 'rotary@fast.com'),
        ('Ryan', 'Runner', '10sec@jdm.com'),
        ('Tia', 'Petrol', 'typer@wtec.com');
        """)
```

<br/>

## 3). Create a route to fetch all patients

```
@app.route('/patients', methods=['GET'])
def get_all_patients():
    patients = None
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute("SELECT * FROM patients;")
        result = curs.fetchall()
        if (len(result) > 0):
            patients = result
    if patients is not None:
        return (patients, 200)
    else:
        return ('No Patients exist!', 404)
```

- create a jinja template for all patients

```
<html>
  <head>
    <title>{{ page }} - {{ sitename }}</title>
  </head>

  <body>
    <h1>{{ sitename }}</h1>
    <h2>{{ page }}</h2>
    <ul>
      {% for patient in patients %}
      <li>{{patient}}</li>
      {% endfor %}
    </ul>
  </body>
</html>
```

edit your route

```
@app.route('/patients', methods=['GET'])
def get_all_patients():
    patients = None
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute("SELECT * FROM patients;")
        result = curs.fetchall()
        if (len(result) > 0):
            patients = result
    if patients is not None:
        return render_template('all_patients.html', patients=patients,sitename='Patient Tracker', page='All Patients')
    else:
        print('line67')
        return 'No Patients exist!', 404
```

<br/>

### 4). Create a route to get one patient by id

```
@app.route('/patients/<int:id>', methods=['GET'])
def get_one_patient(id):
    patient = None
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute(f"SELECT * FROM patients WHERE id={id};")
        result = curs.fetchone()
        patient = result
    if patient is not None:
        return (list(patient), 200)
    else:
        return ('Patient Not Found', 404)
```

- create a jinja template for one patient in templates dir and render it under previously created route

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>{{page}}</title>
  </head>

  <body>
    <h1>{{sitename}}</h1>
    <h2>{{page}}</h2>
    <li>{{patient}}</li>
    <p></p>
  </body>
</html>
```

- modify route

```
@patient_routes.route('/<int:id>', methods=['GET'])
def get_one_patient(id):
    patient = None
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute(f"SELECT * FROM patients WHERE id={id};")
        result = curs.fetchone()
        patient = result
    if patient is not None:
        return render_template("one_patient.html",patient=patient), 200
    else:
        return render_template("one_patient.html", patient
```

<br/>

### 5). Create a Form to Create a New Patient

[FLASK WTF Docs](https://flask.palletsprojects.com/en/3.0.x/patterns/wtforms/)
[WTForms Docs](https://wtforms.readthedocs.io/en/3.1.x/)

- create a new directory in app called forms
- create a new file called create_patient.py
- import flask_wtf for our base form class
- import data fields and validators you would like to use

```
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
```

- Create your form

```
class PatientForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    submit = SubmitField('Create Patient')
```

- Create jinja template to hold form

```
<html>
  <head>
    <title>Create Patient</title>
  </head>

  <body>
    <h1>Create Patient</h1>

    <form action="/patients" method="post" novalidate>
      {{ form.hidden_tag() }}
      <p>{{ form.first_name.label }} {{ form.first_name(size=32) }}</p>
      <p>{{ form.last_name.label }} {{ form.last_name(size=32) }}</p>
      <p>{{ form.email.label }} {{ form.email}}</p>
      <p>{{ form.submit() }}</p>
    </form>
  </body>
</html>

```

- import form to init py
- Create a route to render form /patients/create

```
from .forms.create_patient import PatientForm


@app.route('/patients/create', methods=['GET'])
def get_patient_form():
    form = PatientForm()
    return render_template('create_patient.html', form=form)

```

- create a route to handle your post

```
@app.route('/patients', methods=['POST'])
def post_patient():
    form = PatientForm()
    if form.validate_on_submit():
        with sqlite3.connect(DB_FILE) as conn:
            curs = conn.cursor()
            curs.execute(
        """INSERT INTO patients (first_name, last_name, email)
        VALUES (?, ?, ?)""",
        (form.data['first_name'], form.data['last_name'], form.data['email'])
    )
        return redirect('/patients'. 200)
```

- add validators to your form

```
from wtforms.validators import DataRequired, Email

class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Create Patient')

```

- edit your jinja template to account for validators

```
<html>
  <head>
    <title>Create Patient</title>
  </head>

  <body>
    <h1>Create Patient</h1>

    <form action="/patients/" method="post" novalidate>
      {{ form.hidden_tag() }}
      <p>
        {{ form.first_name.label }}
        {{ form.first_name(size=32) }}
        {% for error in form.first_name.errors %}
          <span style="color: red;">{{ error }}</span>
        {% endfor %}
      </p>
      <p>
        {{ form.last_name.label }}
        {{ form.last_name(size=32) }}
        {% for error in form.last_name.errors %}
          <span style="color: red;">{{ error }}</span>
        {% endfor %}
      </p>
      <p>
        {{ form.email.label }}
        {{ form.email }}
        {% for error in form.email.errors %}
          <span style="color: red;">{{ error }}</span>
        {% endfor %}
      </p>
      <p>{{ form.submit() }}</p>
    </form>
  </body>
</html>
```

- edit your route to handle error validation

```
@app.route('/patients', methods=['POST'])
def post_patient():
    form = PatientForm()
    if form.validate_on_submit():
        with sqlite3.connect(DB_FILE) as conn:
            curs = conn.cursor()
            curs.execute(
        """INSERT INTO patients (first_name, last_name, email)
        VALUES (?, ?, ?)""",
        (form.data['first_name'], form.data['last_name'], form.data['email'])
    )
        return redirect('/patients')

    return render_template('create_patient.html', form=form)
```

<br/>

## 6). Move All Patient Routes to a blueprint

- create a routes dir
- create a patients.py file

```
from flask import (Flask, Blueprint ,render_template, redirect)
from ..forms.create_patient import PatientForm

import sqlite3

DB_FILE = "../dev.db"


patient_routes = Blueprint('patients', __name__)

@patient_routes.route('/', methods=['GET'])
def get_all_patients():
    patients = None
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute("SELECT * FROM patients;")
        result = curs.fetchall()
        if (len(result) > 0):
            patients = result
    if patients is not None:
        return render_template('all_patients.html', patients=patients,sitename='Patient Tracker', page='All Patients')
    else:
        print('line67')
        return 'No Patients exist!', 404

@patient_routes.route('/<int:id>', methods=['GET'])
def get_one_patient(id):
    patient = None
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute(f"SELECT * FROM patients WHERE id={id};")
        result = curs.fetchone()
        patient = result
    if patient is not None:
        return (list(patient), 200)
    else:
        return ('Patient Not Found', 404)

@patient_routes.route('/create', methods=['GET'])
def get_patient_form():
    form = PatientForm()
    return render_template('create_patient.html', form=form), 200

@patient_routes.route('/', methods=['POST'])
def post_patient():
    form = PatientForm()
    if form.validate_on_submit():
        with sqlite3.connect(DB_FILE) as conn:
            curs = conn.cursor()
            curs.execute(
        """INSERT INTO patients (first_name, last_name, email)
        VALUES (?, ?, ?)""",
        (form.data['first_name'], form.data['last_name'], form.data['email'])
    )
        return redirect('/patients')

    return render_template('create_patient.html', form=form)
```

- register blueprint on init py

```
from .routes.patients import patient_routes
app.register_blueprint(patient_routes, url_prefix='/patients')
```

<br/>

## 7). Create a base.html nav bar template and include it on all of our templates

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='index.css')}}"
    />
    <title>Patient Tracker</title>
  </head>
  <body>
    <h1>Patient Tracker</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/patients">All Patients</a>
      <a href="/patients/create">New Patient</a>
    </nav>
    {% block main %} {% endblock %}
  </body>
</html>
```

- extend this base.html to every template you would like using this syntax

```
{% extends "base.html" %}
{% block main %}
things to wrap
{% endblock %}
```

## 8). **Bonus** Create a search bar (patiend id) by using query params and modifying our get all patients route.

- create jinja template for search form

```
<body>
  <form action="/patients" method="get">
    <label for="search">Search by Patient ID:</label>
    <input type="text" id="search" name="id" />
    <input type="submit" value="Search" />
  </form>
</body>
```

- include this form on our base.html

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='index.css')}}"
    />
    <title>Patient Tracker</title>
  </head>
  <body>
    <h1>Patient Tracker</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/patients">All Patients</a>
      <a href="/patients/create">New Patient</a>

      <!-- START -->
      {% include 'search.html' %}
      <!-- END -->

    </nav>
    {% block main %} {% endblock %}
  </body>
</html>
```

- modify all patients route to check for query params, and render one_patient.html if present

```
@patient_routes.route('/', methods=['GET'])
def get_all_patients():

# START
    patiend_id = request.args.get('id')
    if patiend_id is not None:
        return redirect(f'/patients/{patiend_id}')
# END

    patients = None
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute("SELECT * FROM patients;")
        result = curs.fetchall()
        if (len(result) > 0):
            patients = result
    if patients is not None:
            # print('line 47', patients)
            return render_template('all_patients.html', page='All Patients', sitename='Patient Tracker', patients=patients)
    else:
        return 'No Patients exist!'
```
