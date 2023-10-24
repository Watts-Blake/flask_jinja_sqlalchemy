import sqlite3
from flask import (Flask,session, render_template, redirect, Blueprint, request)
from ..forms.create_patient import PatientForm
DB_FILE = '../dev.db'
from ..models import db, Patient


patient_routes = Blueprint('patients', __name__)

@patient_routes.route('/', methods=['GET'])
def get_all_patients():
    patiend_id = request.args.get('id')
    if patiend_id is not None:
        return redirect(f'/patients/{patiend_id}')

    patients = None
    all_patients = Patient.query.all()
    if (len(all_patients) > 0):
            patients = [patient.to_dict() for patient in all_patients]
    if patients is not None:
            return render_template('all_patients.html', page='All Patients', sitename='Patient Tracker', patients=patients)
    else:
        return 'No Patients exist!'

@patient_routes.route('/<int:id>', methods=['GET'])
def get_one_patient(id):
    patient = None

    result = Patient.query.filter(Patient.id == id).first()
    patient = result
    if patient is not None:
        return render_template("one_patient.html",patient=patient.to_dict()), 200
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

        new_patient = Patient(first_name=form.data['first_name'],last_name=form.data['last_name'], email=form.data['email'])
        db.session.add(new_patient)
        db.session.commit()
        return redirect('/patients')
    else:
        return render_template('create_patient.html', form=form)
