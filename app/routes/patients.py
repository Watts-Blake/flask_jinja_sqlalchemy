import sqlite3
from flask import (Flask, render_template, redirect, Blueprint, request)
from ..forms.create_patient import PatientForm
DB_FILE = '../dev.db'


patient_routes = Blueprint('patients', __name__)

@patient_routes.route('/', methods=['GET'])
def get_all_patients():
    patiend_id = request.args.get('id')
    if patiend_id is not None:
        return redirect(f'/patients/{patiend_id}')

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
        return render_template("one_patient.html", patient='Patient Not Found'),404

@patient_routes.route('/create', methods=['GET'])
def get_create_patient_form():
    form = PatientForm()
    return render_template('create_patient.html', form=form)

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
    else:
        return render_template('create_patient.html', form=form)
