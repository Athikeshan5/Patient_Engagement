from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
    UserMixin,
)
from werkzeug.security import generate_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10))  # 'doctor' or 'patient'
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    # Relationships
    doctor_details = db.relationship('DoctorDetails', backref='user', uselist=False)
    health_history = db.relationship('HealthHistory', backref='user', uselist=False)

class DoctorDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Personal Information
    full_name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    profile_photo = db.Column(db.String(100))  # Path to uploaded photo (if implemented)

    # Qualifications
    degree = db.Column(db.String(100))
    certifications = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    license_number = db.Column(db.String(50))

    # Specialization
    specialty = db.Column(db.String(100))
    subspecialty = db.Column(db.String(100))

    # Consultation Details
    consultation_fees = db.Column(db.Float)
    payment_methods = db.Column(db.String(200))
    insurance_accepted = db.Column(db.String(200))

    # Availability
    working_days = db.Column(db.String(100))
    working_hours = db.Column(db.String(100))
    emergency_availability = db.Column(db.String(10))

    # Location
    clinic_name = db.Column(db.String(150))
    clinic_address = db.Column(db.Text)
    telemedicine_services = db.Column(db.String(10))

    # Languages
    languages_spoken = db.Column(db.String(200))

class HealthHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Personal Information
    full_name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))

    # Medical History
    high_blood_pressure = db.Column(db.String(10))  # 'yes' or 'no'
    blood_pressure_rate = db.Column(db.String(20))
    diabetes = db.Column(db.String(10))  # 'yes' or 'no'
    glucose_level = db.Column(db.String(20))
    allergies = db.Column(db.String(10))  # 'yes' or 'no'
    allergy_info = db.Column(db.Text)

    # Family History
    family_heart_disease = db.Column(db.String(10))  # 'yes' or 'no'
    family_cancer = db.Column(db.String(10))  # 'yes' or 'no'

    # Lifestyle
    smoke = db.Column(db.String(10))  # 'yes' or 'no'
    alcohol = db.Column(db.String(10))  # 'yes' or 'no'

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('user-type')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, role=role).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle form submission
        data = request.get_json()
        role = data.get('userType')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        hashed_password = generate_password_hash(password)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Email address already exists'})

        new_user = User(role=role, name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return jsonify({'success': True})

    # Handle GET request to render the signup page
    return render_template('signup.html')


    # Return success response
@app.route('/doctor_details', methods=['GET', 'POST'])
@login_required
def doctor_details():
    if current_user.role != 'doctor':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Personal Information
        full_name = request.form.get('doctor-name')
        email = request.form.get('doctor-email')
        phone = request.form.get('doctor-phone')
        gender = request.form.get('doctor-gender')
        # Profile photo handling can be implemented here

        # Qualifications
        degree = request.form.get('doctor-degree')
        certifications = request.form.get('doctor-certifications')
        experience_years = request.form.get('doctor-experience')
        license_number = request.form.get('doctor-license')

        # Specialization
        specialty = request.form.get('doctor-specialization')
        subspecialty = request.form.get('doctor-subspecialty')

        # Consultation Details
        consultation_fees = request.form.get('doctor-fees')
        payment_methods = request.form.get('doctor-payment-methods')
        insurance_accepted = request.form.get('doctor-insurance')

        # Availability
        working_days = request.form.get('doctor-working-hours')
        working_hours = request.form.get('doctor-working-time')
        emergency_availability = request.form.get('doctor-emergency')

        # Location
        clinic_name = request.form.get('doctor-clinic')
        clinic_address = request.form.get('doctor-address')
        telemedicine_services = request.form.get('doctor-telemedicine')

        # Languages
        languages_spoken = request.form.get('doctor-languages')

        # Save to database
        doctor_details = DoctorDetails(
            user_id=current_user.id,
            full_name=full_name,
            email=email,
            phone=phone,
            gender=gender,
            degree=degree,
            certifications=certifications,
            experience_years=experience_years,
            license_number=license_number,
            specialty=specialty,
            subspecialty=subspecialty,
            consultation_fees=consultation_fees,
            payment_methods=payment_methods,
            insurance_accepted=insurance_accepted,
            working_days=working_days,
            working_hours=working_hours,
            emergency_availability=emergency_availability,
            clinic_name=clinic_name,
            clinic_address=clinic_address,
            telemedicine_services=telemedicine_services,
            languages_spoken=languages_spoken
        )
        db.session.add(doctor_details)
        db.session.commit()

        flash('Doctor details saved successfully', 'success')
        return redirect(url_for('logout'))

    return render_template('doctor_details.html')

@app.route('/health_history', methods=['GET', 'POST'])
@login_required
def health_history():
    if current_user.role != 'patient':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Personal Information
        full_name = request.form.get('full-name')
        age = request.form.get('age')
        gender = request.form.get('gender')

        # Medical History
        high_blood_pressure = request.form.get('blood-pressure')
        blood_pressure_rate = request.form.get('pressure-rate-input')
        diabetes = request.form.get('diabetes')
        glucose_level = request.form.get('glucose-level')
        allergies = request.form.get('allergies')
        allergy_info = request.form.get('allergy-info')

        # Family History
        family_heart_disease = request.form.get('family-heart-disease')
        family_cancer = request.form.get('family-cancer')

        # Lifestyle
        smoke = request.form.get('smoke')
        alcohol = request.form.get('alcohol')

        # Save to database
        health_history = HealthHistory(
            user_id=current_user.id,
            full_name=full_name,
            age=age,
            gender=gender,
            high_blood_pressure=high_blood_pressure,
            blood_pressure_rate=blood_pressure_rate,
            diabetes=diabetes,
            glucose_level=glucose_level,
            allergies=allergies,
            allergy_info=allergy_info,
            family_heart_disease=family_heart_disease,
            family_cancer=family_cancer,
            smoke=smoke,
            alcohol=alcohol
        )
        db.session.add(health_history)
        db.session.commit()

        flash('Health history saved successfully', 'success')
        return redirect(url_for('logout'))

    return render_template('health_history.html')

@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))

    doctor_details = current_user.doctor_details
    return render_template('doctor_dashboard.html', doctor_details=doctor_details)

@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
    if current_user.role != 'patient':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))

    health_history = current_user.health_history
    return render_template('patient_dashboard.html', health_history=health_history)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)

