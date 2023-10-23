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
- Edit all of our database connections to use SQLAlchemy instead of sqlite3

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
class Patient(db.Model, UserMixin):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
```
