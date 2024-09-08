from flask import Flask, render_template, abort, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Time, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = "Secret Key"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://eisenchamp:mysqlassignment@eisenchamp.mysql.pythonanywhere-services.com/eisenchamp$Assignment'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/Assignment 2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Base = declarative_base()

class USER(Base):
    __tablename__ = 'USER'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    given_name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    city = Column(String(100))
    phone_number = Column(String(20))
    profile_description = Column(Text)
    password = Column(String(255), nullable=False)

    def __init__(self, email, given_name, surname, city=None, phone_number=None, profile_description=None, password=None):
        self.email = email
        self.given_name = given_name
        self.surname = surname
        self.city = city
        self.phone_number = phone_number
        self.profile_description = profile_description
        self.password = password

    def __repr__(self):
        return f"<USER(user_id={self.user_id}, email={self.email}, given_name={self.given_name}, surname={self.surname})>"

class CAREGIVER(USER, Base):
    __tablename__ = 'CAREGIVER'
    caregiver_user_id = Column(Integer, ForeignKey('USER.user_id'), primary_key=True)
    photo = Column(String(255))
    gender = Column(String(10))
    caregiving_type = Column(String(100))
    hourly_rate = Column(Float) 

    appointments = relationship('APPOINTMENT', back_populates='caregiver')

    def __init__(self, email, given_name, surname, photo, gender, caregiving_type, hourly_rate, city=None, phone_number=None, profile_description=None, password=None):
        super().__init__(email, given_name, surname, city, phone_number, profile_description, password)
        self.caregiver_user_id = self.user_id
        self.photo = photo
        self.gender = gender
        self.caregiving_type = caregiving_type
        self.hourly_rate = hourly_rate

    def __repr__(self):
        return f"<CAREGIVER(caregiver_user_id={self.caregiver_user_id}, photo={self.photo}, gender={self.gender}, caregiving_type={self.caregiving_type}, hourly_rate={self.hourly_rate})>"
    
class MEMBER(USER, Base):
    __tablename__ = 'MEMBER'
    member_user_id = Column(Integer, ForeignKey('USER.user_id'), primary_key=True)
    house_rules = Column(Text)

    jobs = relationship('JOB', back_populates='member')

    address = relationship('ADDRESS', back_populates='member', uselist=False)

    appointments = relationship('APPOINTMENT', back_populates='member')

    def __init__(self, email, given_name, surname, house_rules, city=None, phone_number=None, profile_description=None, password=None):
        super().__init__(email, given_name, surname, city, phone_number, profile_description, password)
        self.member_user_id = self.user_id
        self.house_rules = house_rules

    def __repr__(self):
        return f"<MEMBER(member_user_id={self.member_user_id}, house_rules={self.house_rules})>"



class ADDRESS(Base):
    __tablename__ = 'ADDRESS'
    member_user_id = Column(Integer, ForeignKey('MEMBER.member_user_id'), primary_key=True)
    house_number = Column(String(20))
    street = Column(String(100))
    town = Column(String(100))

    member = relationship('MEMBER', back_populates='address')

    def __init__(self, member_user_id, house_number, street, town):
        self.member_user_id = member_user_id
        self.house_number = house_number
        self.street = street
        self.town = town

    def __repr__(self):
        return f"<ADDRESS(member_user_id={self.member_user_id}, house_number={self.house_number}, street={self.street}, town={self.town})>"

class JOB(Base):
    __tablename__ = 'JOB'
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    member_user_id = Column(Integer, ForeignKey('MEMBER.member_user_id'))
    required_caregiving_type = Column(String(50))
    other_requirements = Column(Text)
    date_posted = Column(Date)

    member = relationship('MEMBER', back_populates='jobs')

    def __init__(self, member_user_id, required_caregiving_type, other_requirements, date_posted):
        self.member_user_id = member_user_id
        self.required_caregiving_type = required_caregiving_type
        self.other_requirements = other_requirements
        self.date_posted = date_posted

    def __repr__(self):
        return f"<JOB(job_id={self.job_id}, member_user_id={self.member_user_id}, required_caregiving_type={self.required_caregiving_type}, date_posted={self.date_posted})>"

class JOB_APPLICATION(Base):
    __tablename__ = 'JOB_APPLICATION'
    caregiver_user_id = Column(Integer, ForeignKey('CAREGIVER.caregiver_user_id'), primary_key=True)
    job_id = Column(Integer, ForeignKey('JOB.job_id'), primary_key=True)
    date_applied = Column(Date)

    def __init__(self, caregiver_user_id, job_id, date_applied):
        self.caregiver_user_id = caregiver_user_id
        self.job_id = job_id
        self.date_applied = date_applied

    def __repr__(self):
        return f"<JOB_APPLICATION(caregiver_user_id={self.caregiver_user_id}, job_id={self.job_id}, date_applied={self.date_applied})>"

class APPOINTMENT(Base):
    __tablename__ = 'APPOINTMENT'
    appointment_id = Column(Integer, primary_key=True)
    caregiver_user_id = Column(Integer, ForeignKey('CAREGIVER.caregiver_user_id'))
    member_user_id = Column(Integer, ForeignKey('MEMBER.member_user_id'))
    appointment_date = Column(Date)
    appointment_time = Column(Time)
    work_hours = Column(Float)
    status = Column(String(50))
    
    caregiver = relationship('CAREGIVER', back_populates='appointments')

    member = relationship('MEMBER', back_populates='appointments')

    def __init__(self, caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status):
        self.caregiver_user_id = caregiver_user_id
        self.member_user_id = member_user_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.work_hours = work_hours
        self.status = status

    def __repr__(self):
        return f"<APPOINTMENT(appointment_id={self.appointment_id}, caregiver_user_id={self.caregiver_user_id}, member_user_id={self.member_user_id}, appointment_date={self.appointment_date}, appointment_time={self.appointment_time}, work_hours={self.work_hours}, status={self.status})>"
    

@app.route('/')
def Index():
    mem_data = db.session.query(MEMBER).all()
    care_data = db.session.query(CAREGIVER).all()
    appoint_data = db.session.query(APPOINTMENT).all()

    return render_template("index.html", caregivers = care_data, members = mem_data, appointments = appoint_data)


@app.route('/insert/member', methods = ['POST'])
def insert_member():
    if request.method == 'POST':
        email = request.form['email']
        given_name = request.form['given_name']
        surname = request.form['surname']
        city = request.form['city']
        phone = request.form['phone_number']
        profile_description = request.form['profile_description']
        password = request.form['password']
        house_rules = request.form['house_rules']

        my_data = MEMBER(email, given_name, surname, house_rules, city, phone, profile_description, password)
        db.session.add(my_data)
        db.session.commit()

        flash("Member Inserted Successfully")

        return redirect(url_for('Index'))
    
@app.route('/update/member', methods=['GET', 'POST'])
def update_member():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        my_data = db.session.query(MEMBER).get(user_id)

        if my_data:
            my_data.email = request.form['email']
            my_data.given_name = request.form['given_name']
            my_data.surname = request.form['surname']
            my_data.house_rules = request.form['house_rules']
            my_data.city = request.form['city']
            my_data.phone = request.form['phone_number']
            my_data.profile_description = request.form['profile_description']
            my_data.password = request.form['password']

            db.session.commit()
            flash("Member Updated Successfully")
        else:
            flash(f"Member with ID {user_id} not found")

        return redirect(url_for('Index'))
    

@app.route('/delete/<user_id>/', methods = ['GET', 'POST'])
def delete_member(user_id):
    my_data = db.session.query(USER).get(user_id)
    if my_data:
        db.session.delete(my_data)
        db.session.commit()
    else:
        my_data = db.session.query(APPOINTMENT).get(user_id)
        db.session.delete(my_data)
        db.session.commit()
    flash("User Was Deleted")

    return redirect(url_for('Index'))


@app.route('/insert/caregiver', methods = ['POST'])
def insert_caregiver():
    if request.method == 'POST':
        email = request.form['email']
        given_name = request.form['given_name']
        surname = request.form['surname']
        city = request.form['city']
        phone = request.form['phone_number']
        profile_description = request.form['profile_description']
        password = request.form['password']
        photo = request.form['photo']
        gender = request.form['gender']
        caregiving_type = request.form['caregiving_type']
        hourly_rate = request.form['hourly_rate']

        my_data = CAREGIVER(email, given_name, surname, photo, gender, caregiving_type, hourly_rate, city, phone, profile_description, password)
        db.session.add(my_data)
        db.session.commit()

        flash("Caregiver Inserted Successfully")

        return redirect(url_for('Index'))
    
@app.route('/update/caregiver', methods=['GET', 'POST'])
def update_caregiver():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        my_data = db.session.query(CAREGIVER).get(user_id)

        if my_data:
            my_data.email = request.form['email']
            my_data.given_name = request.form['given_name']
            my_data.surname = request.form['surname']
            my_data.photo = request.form['photo']
            my_data.gender = request.form['gender']
            my_data.caregiving_type = request.form['caregiving_type']
            my_data.hourly_rate = request.form['hourly_rate']
            my_data.city = request.form['city']
            my_data.phone = request.form['phone_number']
            my_data.profile_description = request.form['profile_description']
            my_data.password = request.form['password']

            db.session.commit()
            flash("Caregiver Updated Successfully")
        else:
            flash(f"Caregiver with ID {user_id} not found")

        return redirect(url_for('Index'))




@app.route('/insert/appointment', methods = ['POST'])
def insert_appointment():
    if request.method == 'POST':
        caregiver_user_id = request.form['caregiver_user_id']
        member_user_id = request.form['member_user_id']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        work_hours = request.form['work_hours']
        status = request.form['status']

        my_data = APPOINTMENT(caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status)
        db.session.add(my_data)
        db.session.commit()

        flash("Appointment Inserted Successfully")

        return redirect(url_for('Index'))
    
@app.route('/update/appointment', methods=['GET', 'POST'])
def update_appointment():
    if request.method == 'POST':
        user_id = request.form.get('appointment_id')
        my_data = db.session.query(APPOINTMENT).get(user_id)

        if my_data:
            my_data.caregiver_user_id = request.form['caregiver_user_id']
            my_data.member_user_id = request.form['member_user_id']
            my_data.appointment_date = request.form['appointment_date']
            my_data.appointment_time = request.form['appointment_time']
            my_data.work_hours = request.form['work_hours']
            my_data.status = request.form['status']

            db.session.commit()
            flash("Appointment Updated Successfully")
        else:
            flash(f"Appointment with ID {user_id} not found")

        return redirect(url_for('Index'))
    

@app.route('/delete/<user_id>/', methods = ['GET', 'POST'])
def delete_appointment(user_id):
    my_data = db.session.query(APPOINTMENT).get(user_id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Appointment Was Deleted")

    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
