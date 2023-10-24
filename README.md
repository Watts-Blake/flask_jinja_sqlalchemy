# SQL ALCHEMY

## What Were doing

In this lecture we will convert our project from last week which used SQLITE3 to now use SQLALCHEMY instead

### What is SQL Alchemy? [Docs](https://docs.sqlalchemy.org/en/20/)

- SQLAlchemy is an ORM (Object Relational Mapping) similar to when we used Sequelize with Express
- We will use SQLAlchemy to create our sql database with class Objects in python by mapping over them.

## What we need to do

- install dependencies for SQLAlchemy
- Setup our flask application with SQLAlchemy
- Create our Model/Table for our database
- Seed Patients
- Edit all of our database connections to use SQLAlchemy instead of sqlite3
- Edit SqlAlchemy object to have a to_dict method

<br/>

## 1). Install dependencies

### In Terminal Run in root of project

```
pipenv install
pipenv install sqlalchemy flask-sqlalchemy
```

## 2). Setup up our Flask up to use SQLAlchemy

- inside your .env, make sure to add your db url env key

```
DATABASE_URL=sqlite:///dev.db
```

- edit your config file in app to nclude your db uri, and set track modifications to false, to avoid the track warnings on every db connection

```
import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

- Create a models module inside of you app dir

  - inside of that module, create you scqlalchemy instance

```
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

- initialize your app with your newly created db on your app init

```
from .models import db

db.init_app(app)
```

## 3). Create our First Model/Table

- in your models module create a model
- [COLUMN DATATYPES DOCS](https://docs.sqlalchemy.org/en/20/core/types.html)

```
class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
```

## 4). Seed Patients

- create a seeder file in proj root

```
# seeder.py

from app.models import Patient, db  # Import your Patient model and db object

def seed_patients():
    patients = [
        {"first_name": 'Tim', "last_name": 'Petrol', "email": 'rotary@fast.com'},
        {"first_name": 'Ryan', "last_name": 'Runner', "email": '10sec@jdm.com'},
        {"first_name": 'Tia', "last_name": 'Petrol', "email": 'typer@wtec.com'}
    ]

    for patient_data in patients:
        new_patient = Patient(
            first_name=patient_data['first_name'],
            last_name=patient_data['last_name'],
            email=patient_data['email']
        )

        db.session.add(new_patient)
        db.session.commit()

        # Optionally, print the newly added patients for confirmation
        print(f"Added patient: {new_patient}")

# If you want to run this script separately, you can do so with the following code:
if __name__ == '__main__':
    # Import your Flask app and initialize it
    from app import app
    app.app_context().push()

    # Call the seed_patients function
    db.create_all()
    seed_patients()

```

in terminal run

```
python seeder.py
```

## 5). Edit DB Connections in routes

- modify get patients route

```
@patient_routes.route('/', methods=['GET'])
def get_all_patients():
    patiend_id = request.args.get('id')
    if patiend_id is not None:
        return redirect(f'/patients/{patiend_id}')

    patients = None
    all_patients = Patient.query.all()
    if (len(all_patients) > 0):
            patients = all_patients
    if patients is not None:
            return render_template('all_patients.html', page='All Patients', sitename='Patient Tracker', patients=patients)
    else:
        return 'No Patients exist!'
```

- modify get one patient route

```
@patient_routes.route('/<int:id>', methods=['GET'])
def get_one_patient(id):
    patient = None

    result = Patient.query.filter(Patient.id == id).first()
    patient = result
    if patient is not None:
        return render_template("one_patient.html",patient=patient), 200
    else:
        return render_template("one_patient.html", patient='Patient Not Found'),404
```

- modify our post patient route

```
@patient_routes.route('/', methods=['POST'])
def post_patient():
    form = PatientForm()
    if form.validate_on_submit():
        new_patient = Patient(first_name=form.data['first_name'],last_name=form.data['last_name'], email=form.data['email'])
        db.session.add(new_patient)
        db.session.commit()
        return redirect('/patients')
    else:
        return render_template('create_patient.html', form=form)
```

## 6). Modify Model to have a to_dict() method and utilize in routes

- model

```
class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
```

- routes

```
# all patients
 patients = [patient.to_dict() for patient in all_patients]

# one patient
 return render_template("one_patient.html",patient=patient.to_dict()), 200
```

- key into properties of objects on templates
