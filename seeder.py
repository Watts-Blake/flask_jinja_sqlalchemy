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
