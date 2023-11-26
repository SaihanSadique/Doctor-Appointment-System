from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import text
import inspect
from datetime import datetime


# START CONNECTION RELATED CODE
app = Flask(__name__, static_folder="static")
app.secret_key = "6516518941"  # Set a secret key for session
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:12345@localhost/appointmentsystem?charset=latin1"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
# END CONNECTION RELATED CODE
with app.app_context():
    # Perform database operations or anything that requires the app context here
    db.reflect()

    class patient_details(db.Model):
        __table__ = db.Model.metadata.tables["patient"]

    class appointment(db.Model):
        __table__ = db.Model.metadata.tables["appointment"]


# APP ROUTING DECORATORS
@app.route("/")
def reg_page():
    return render_template("LOGIN.html")


@app.route("/login")
def login_page():
    return render_template("LOGIN.html")


@app.route("/dashboard")
def dashboard():
    with app.app_context():
        user_email = session.get("email")
        print("successfully sent user_email data", user_email)
        patient_pid = (
            db.session.query(patient_details.pid)
            .filter(patient_details.email == user_email)
            .scalar()
        )
        results = (
            db.session.query(patient_details, appointment)
            .join(patient_details, patient_pid == appointment.uid)
            .filter(patient_details.pid == patient_pid)
            .all()
        )
    return render_template(
        "DASHBOARD.html"
    )  # ,joined_data=joined_data DONT FORGET TO ADD THIS


# USER CREDENTIAL VALIDATION FUNCTION
def validate_login(retrieved_email, password):
    bool_value_verification = patient_details.query.filter_by(
        email=retrieved_email, password=password
    ).first()
    return bool_value_verification


@app.route("/new-reg")
def newReg():
    return render_template("NEW-REG.html")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("LOGIN.html")


@app.route("/validate-login", methods=["POST"])
def login():
    Email = request.form["Email"]
    password = request.form["password"]
    if validate_login(Email, password):
        user_email = {"email": Email}
        session.update(user_email)
        return redirect("/dashboard")  # Redirect to a dashboard route
    else:
        return render_template("LOGIN.html", error="Invalid username or password")


@app.route("/register_input", methods=["POST"])
def register_input():
    name = request.form["name"]
    email = request.form["email"]
    phone_number = request.form["phone_number"]
    password = request.form["password"]
    with app.app_context():
        new_user = patient_details()
        new_user.name = name
        new_user.email = email
        new_user.password = phone_number
        new_user.phnumber = password
        db.session.add(new_user)
        db.session.commit()
        success_message = "Account Successfully Created!"
    return render_template("LOGIN.html",message = success_message)

@app.route("/new_appointment")
def new_appointment():
    return render_template("NEWAPPOINTMENT.html")

@app.route("/new_post_appointment", methods=["POST"])
def new_post_appointment():
    dateslot = request.form["appointmentDate"]
    timeslot_start = request.form["appointmentTime"]
    selected_purpose = request.form["purpose-select"]
    timeslot_temp = int(timeslot_start[0]+timeslot_start[1])
    timeslot_temp += 2
    timeslot_temp =str(timeslot_temp)
    timeslot_end = list(timeslot_start)
    timeslot_end[0] = timeslot_temp[0]
    timeslot_end[1] = timeslot_temp[1];
    timeslot_end = ''.join(timeslot_end)            # The above code mostly tries its best to adapt to dattime column of MySql, it tried its best
    combined_datetime_start_str = f'{dateslot} {timeslot_start}'
    combined_datetime_end_str = f'{dateslot} {timeslot_end}'
    combined_datetime_start = datetime.strptime(combined_datetime_start_str, "%Y-%m-%d %H:%M")
    combined_datetime_end = datetime.strptime(combined_datetime_end_str, "%Y-%m-%d %H:%M")
    print(combined_datetime_start)
    print(combined_datetime_end)
    
    
    user_email = session.get("email")
    with app.app_context():
        class appointment(db.Model):
            __table__ = db.Model.metadata.tables["appointment"]
        
        # all_appointments = appointment.query.all()
        # for appointmentss in all_appointments:
        #     print(appointmentss.DateTime)
        bool_time_slot_verification = appointment.query.filter(
        appointment.DateTime == combined_datetime_start.date()).first()
        bool_time_slot_verification = appointment.query.filter(appointment.DateTime.between(combined_datetime_start, combined_datetime_end)).first()    
        print(bool_time_slot_verification)
        if bool_time_slot_verification:
            print("has a booking in between")
            return render_template("NEWAPPOINTMENT.html",message='BOOKED')
        else:
            patient_pid = (
            db.session.query(patient_details.pid)
            .filter(patient_details.email == user_email)
            .scalar()
            )
            new_app = appointment()
            new_app.uid = patient_pid
            new_app.DateTime = combined_datetime_start
            db.session.add(new_app)
            db.session.commit()
            success_message = "created new booking!"
            return render_template("DASHBOARD.html",message = success_message)

@app.route('/get_appointments_list')
def get_appointments_list():
    class appointment(db.Model):
        __table__ = db.Model.metadata.tables["appointment"]
    user_email = session.get("email")
    patient_pid = (
            db.session.query(patient_details.pid)
            .filter(patient_details.email == user_email)
            .scalar()
            )
    appointments_list_temp = appointment.query.filter_by(uid=patient_pid).with_entities(appointment.DateTime).all()
    appointments_list = [{'DateTime': appointment.DateTime} for appointment in appointments_list_temp]
    print(appointments_list)
    return jsonify(appointments_list)