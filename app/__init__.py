
from flask import (Flask, render_template, redirect)
from .config import Config
from .models import db, Patient


from .forms.create_patient import PatientForm
from .routes.patients import patient_routes


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)



@app.route('/')
def get_index():
    return render_template('index.html', page='HOME', sitename='Patient Tracker')

app.register_blueprint(patient_routes, url_prefix='/patients')
