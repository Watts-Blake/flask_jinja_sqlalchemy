import sqlite3
from flask import (Flask, render_template, redirect)
from .config import Config
from .forms.create_patient import PatientForm
from .routes.patients import patient_routes

DB_FILE = '../dev.db'
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

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def get_index():
    return render_template('index.html', page='HOME', sitename='Patient Tracker')

app.register_blueprint(patient_routes, url_prefix='/patients')
