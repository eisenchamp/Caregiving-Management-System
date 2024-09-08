from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Time, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy import func

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
    
engine = create_engine('postgresql://postgres:postgres@localhost/Assignment 2')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

 session.query(APPOINTMENT).delete()
 session.query(JOB_APPLICATION).delete()
 session.query(JOB).delete()
 session.query(ADDRESS).delete()
 session.query(MEMBER).delete()
 session.query(CAREGIVER).delete()
 session.query(USER).delete()
 session.commit()

 print("Done Deleting")

 caregiver1 = CAREGIVER(email='ariana.grande@google.com', given_name='Ariana', surname='Grande', phone_number='+732963298325423', password='Positions', photo='photo1.jpg', gender='Female', caregiving_type='Elderly Care', hourly_rate=20.0, city='New York', profile_description='Can cook, clean, sing and take care of others')
 caregiver2 = CAREGIVER(email='doja.cat@icloud.com', given_name='Doja', surname='Cat', phone_number='+8373489297489374097', password='PaintTheTownRed', photo='photo2.jpg', gender='Female', caregiving_type='Babysitter', hourly_rate=8.0, city='Washington', profile_description='Can cook, clean, rap and take care of others')
 caregiver3 = CAREGIVER(email='travis.scott@google.com', given_name='Travis', surname='Scott', phone_number='+8374894793749823', password='HYENA', photo='photo3.jpg', gender='Male', caregiving_type='Elderly Care', hourly_rate=11.0, city='Niagara Falls', profile_description='Can cook, rap, clean and take care of others')
 caregiver4 = CAREGIVER(email='adele@google.com', given_name='Adele', surname='Adele', phone_number='+78456539384793', password='SetFiretotheRain', photo='photo4.jpg', gender='Female', caregiving_type='Playmate for children', hourly_rate=15.4, city='Almaty', profile_description='Can cook, clean, sing, and take care of others')
 caregiver5 = CAREGIVER(email='billie.eilish@google.com', given_name='Billie', surname='Eilish', phone_number='+83737649362', password='BillieBossaNova', photo='photo5.jpg', gender='Female', caregiving_type='Babysitter', hourly_rate=8.8, city='Karaganda', profile_description='Can cook, clean, sing and take care of others')
 caregiver6 = CAREGIVER(email='bren.joy@google.com', given_name='Bren', surname='Joy', phone_number='+76378462984792', password='Sweet', photo='photo6.jpg', gender='Male', caregiving_type='Elderly Care', hourly_rate=19.0, city='Astana', profile_description='Can cook, clean, rap and take care of others')
 caregiver7 = CAREGIVER(email='brent.feiyaz@icloud.com', given_name='Brent', surname='Feiyaz', phone_number='+83275892738045872', password='Trust', photo='photo7.jpg', gender='Male', caregiving_type='Playmate for children', hourly_rate=16.7, city='Astana', profile_description='Can cook, clean, sing and take care of others')
 caregiver8 = CAREGIVER(email='bad.bunny@google.com', given_name='Bad', surname='Bunny', phone_number='+3827573267523', password='MePortoBonito', photo='photo8.jpg', gender='Male', caregiving_type='Elderly Care', hourly_rate=23.0, city='Karaganda', profile_description='Can cook, clean, rap and take care of others')
 caregiver9 = CAREGIVER(email='askar@example.com', given_name='Askar', surname='Askarov', phone_number='+02983938832983', password='securepassword', photo='photo9.jpg', gender='Male', caregiving_type='Babysitter', hourly_rate=18.5, city='Taraz', profile_description='Can cook, clean, sing, rap and take care of others')
 caregiver10 = CAREGIVER(email='frank.ocean@google.com', given_name='Frank', surname='Ocean', phone_number='+84687484968274', password='Blonde', photo='photo10.jpg', gender='Male', caregiving_type='Playmate for children', hourly_rate=25.0, city='Shymkent', profile_description='Can cook, clean, sing and take care of others')

 session.add(caregiver1)
 session.add(caregiver2)
 session.add(caregiver3)
 session.add(caregiver4)
 session.add(caregiver5)
 session.add(caregiver6)
 session.add(caregiver7)
 session.add(caregiver8)
 session.add(caregiver9)
 session.add(caregiver10)
 session.commit()
 print("Caregivers added")

 member1 = MEMBER(email='kali.uchis@google.com', given_name='Kali', surname='Uchis', phone_number='+9047534705933', password='Moonlight', house_rules='No pets')
 member2 = MEMBER(email='dua.lipa@google.com', given_name='Dua', surname='Lipa', phone_number='+832975983421', password='Hudini', house_rules='Pet Friendly')
 member3 = MEMBER(email='ed.sheeran@google.com', given_name='Ed', surname='Sheeran', phone_number='+3207590435', password='ShapeOfYou', house_rules='Quite time from 6pm to 9am')
 member4 = MEMBER(email='mariah.carey@google.com', given_name='Mariah', surname='Carey', phone_number='+83275893203', password='AllIWantForChristmas', house_rules='No pets')
 member5 = MEMBER(email='metro.boomin@google.com', given_name='Metro', surname='Boomin', phone_number='+8375326592344', password='Creepin', house_rules='Pet Friendly')
 member6 = MEMBER(email='post.malone@google.com', given_name='Post', surname='Malone', phone_number='+372423598332', password='Circles', house_rules='No pets')
 member7 = MEMBER(email='shawn.mandes@google.com', given_name='Shawn', surname='Mandes', phone_number='+3756765923423', password='HoldingMeBack', house_rules='Pet Friendly')
 member8 = MEMBER(email='tai.verdes@google.com', given_name='Tai', surname='Verdes', phone_number='+7435234623946', password='HowDeep', house_rules='No pets')
 member9 = MEMBER(email='tory.lanez@google.com', given_name='Tory', surname='Lanez', phone_number='+9461267424813', password='HurtsMe', house_rules='Quite time from 6pm to 9am')
 member10 = MEMBER(email='bolat.bolatov@google.com', given_name='Bolat', surname='Bolatov', phone_number='+7702384029435', password='Pettypretty', house_rules='No pets')

 session.add(member1)
 session.add(member2)
 session.add(member3)
 session.add(member4)
 session.add(member5)
 session.add(member6)
 session.add(member7)
 session.add(member8)
 session.add(member9)
 session.add(member10)
 session.commit()
 print("Members added")

 member1.address = ADDRESS(member_user_id=member1.member_user_id, house_number='5', street='Turan', town='Astana')
 member2.address = ADDRESS(member_user_id=member2.member_user_id, house_number='64', street='Barrington', town='Ocean City')
 member3.address = ADDRESS(member_user_id=member3.member_user_id, house_number='43', street='Copper', town='Aspen')
 member4.address = ADDRESS(member_user_id=member4.member_user_id, house_number='52', street='Broadway', town='New York')
 member5.address = ADDRESS(member_user_id=member5.member_user_id, house_number='123', street='Turan', town='Astana')
 member6.address = ADDRESS(member_user_id=member6.member_user_id, house_number='877', street='Kabanbay', town='Astana')
 member7.address = ADDRESS(member_user_id=member7.member_user_id, house_number='53', street='Abai', town='Almaty')
 member8.address = ADDRESS(member_user_id=member8.member_user_id, house_number='75', street='Buhar Zhyrau', town='Karaganda')
 member9.address = ADDRESS(member_user_id=member9.member_user_id, house_number='54', street='LimeLight', town='Denver')
 member10.address = ADDRESS(member_user_id=member10.member_user_id, house_number='32', street='Kerey Zhanibek', town='Astana')

 session.add(member1)
 session.add(member2)
 session.add(member3)
 session.add(member4)
 session.add(member5)
 session.add(member6)
 session.add(member7)
 session.add(member8)
 session.add(member9)
 session.add(member10)
 session.commit()
 print("Address added")

 job1 = JOB(member_user_id=member1.member_user_id, required_caregiving_type='Elderly Care', other_requirements='gentle with elderly individuals preferred', date_posted='2023-03-20')
 job2 = JOB(member_user_id=member2.member_user_id, required_caregiving_type='Babysitter', other_requirements='Experience with babies preferred', date_posted='2023-04-24')
 job3 = JOB(member_user_id=member3.member_user_id, required_caregiving_type='Playmate for children', other_requirements='Experience with children individuals preferred', date_posted='2023-06-18')
 job4 = JOB(member_user_id=member1.member_user_id, required_caregiving_type='Babysitter', other_requirements='Experience with gentle babies preferred', date_posted='2023-05-05')
 job5 = JOB(member_user_id=member10.member_user_id, required_caregiving_type='Elderly Care', other_requirements='Experience with elderly individuals preferred', date_posted='2023-09-13')
 job6 = JOB(member_user_id=member10.member_user_id, required_caregiving_type='Playmate for children', other_requirements='Experience with gentle children individuals preferred', date_posted='2023-11-06')
 job7 = JOB(member_user_id=member6.member_user_id, required_caregiving_type='Elderly Care', other_requirements='Experience with elderly individuals preferred', date_posted='2023-03-26')
 job8 = JOB(member_user_id=member4.member_user_id, required_caregiving_type='Playmate for children', other_requirements='gentle Experience with children individuals preferred', date_posted='2022-12-31')
 job9 = JOB(member_user_id=member8.member_user_id, required_caregiving_type='Babysitter', other_requirements='Experience with babies preferred', date_posted='2023-10-23')
 job10 = JOB(member_user_id=member9.member_user_id, required_caregiving_type='Elderly Care', other_requirements='Experience with gentle elderly individuals preferred', date_posted='2022-12-14')

 session.add(job1)
 session.add(job2)
 session.add(job3)
 session.add(job4)
 session.add(job5)
 session.add(job6)
 session.add(job7)
 session.add(job8)
 session.add(job9)
 session.add(job10)
 session.commit()
 print("Jobs added")

 job_application1 = JOB_APPLICATION(caregiver_user_id=caregiver1.caregiver_user_id, job_id=job1.job_id, date_applied='2023-11-7')
 job_application2 = JOB_APPLICATION(caregiver_user_id=caregiver1.caregiver_user_id, job_id=job4.job_id, date_applied='2023-12-7')
 job_application3 = JOB_APPLICATION(caregiver_user_id=caregiver4.caregiver_user_id, job_id=job5.job_id, date_applied='2022-12-31')
 job_application4 = JOB_APPLICATION(caregiver_user_id=caregiver5.caregiver_user_id, job_id=job7.job_id, date_applied='2023-09-23')
 job_application5 = JOB_APPLICATION(caregiver_user_id=caregiver2.caregiver_user_id, job_id=job8.job_id, date_applied='2023-05-14')
 job_application6 = JOB_APPLICATION(caregiver_user_id=caregiver9.caregiver_user_id, job_id=job5.job_id, date_applied='2022-10-06')
 job_application7 = JOB_APPLICATION(caregiver_user_id=caregiver6.caregiver_user_id, job_id=job6.job_id, date_applied='2023-09-04')
 job_application8 = JOB_APPLICATION(caregiver_user_id=caregiver10.caregiver_user_id, job_id=job9.job_id, date_applied='2023-07-03')
 job_application9 = JOB_APPLICATION(caregiver_user_id=caregiver9.caregiver_user_id, job_id=job10.job_id, date_applied='2023-08-30')
 job_application10 = JOB_APPLICATION(caregiver_user_id=caregiver8.caregiver_user_id, job_id=job8.job_id, date_applied='2023-05-15')

 session.add(job_application1)
 session.add(job_application2)
 session.add(job_application3)
 session.add(job_application4)
 session.add(job_application5)
 session.add(job_application6)
 session.add(job_application7)
 session.add(job_application8)
 session.add(job_application9)
 session.add(job_application10)
 session.commit()
 print("Job applications added")

 appointment1 = APPOINTMENT(caregiver_user_id=caregiver1.caregiver_user_id, member_user_id=member1.member_user_id, appointment_date='2023-11-10', appointment_time='14:00:00', work_hours=3.5, status="Scheduled")
 appointment2 = APPOINTMENT(caregiver_user_id=caregiver3.caregiver_user_id, member_user_id=member2.member_user_id, appointment_date='2023-07-23', appointment_time='15:30:00', work_hours=8.5, status="Rejected")
 appointment3 = APPOINTMENT(caregiver_user_id=caregiver4.caregiver_user_id, member_user_id=member10.member_user_id, appointment_date='2023-09-10', appointment_time='11:20:00', work_hours=5.0, status="Accepted")
 appointment4 = APPOINTMENT(caregiver_user_id=caregiver5.caregiver_user_id, member_user_id=member5.member_user_id, appointment_date='2022-07-17', appointment_time='15:12:00', work_hours=2.0, status="Scheduled")
 appointment5 = APPOINTMENT(caregiver_user_id=caregiver5.caregiver_user_id, member_user_id=member8.member_user_id, appointment_date='2023-09-19', appointment_time='18:36:00', work_hours=4.5, status="Rejected")
 appointment6 = APPOINTMENT(caregiver_user_id=caregiver1.caregiver_user_id, member_user_id=member3.member_user_id, appointment_date='2023-04-24', appointment_time='14:45:00', work_hours=3.5, status="Accepted")
 appointment7 = APPOINTMENT(caregiver_user_id=caregiver2.caregiver_user_id, member_user_id=member5.member_user_id, appointment_date='2023-12-30', appointment_time='16:34:00', work_hours=5.5, status="Accepted")
 appointment8 = APPOINTMENT(caregiver_user_id=caregiver5.caregiver_user_id, member_user_id=member2.member_user_id, appointment_date='2023-11-23', appointment_time='13:36:00', work_hours=6.0, status="Rejected")
 appointment9 = APPOINTMENT(caregiver_user_id=caregiver8.caregiver_user_id, member_user_id=member6.member_user_id, appointment_date='2023-07-15', appointment_time='16:25:00', work_hours=3.0, status="Rejected")
 appointment10 = APPOINTMENT(caregiver_user_id=caregiver10.caregiver_user_id, member_user_id=member9.member_user_id, appointment_date='2023-04-27', appointment_time='17:14:00', work_hours=4.5, status="Accepted")


 session.add(appointment1)
 session.add(appointment2)
 session.add(appointment3)
 session.add(appointment4)
 session.add(appointment5)
 session.add(appointment6)
 session.add(appointment7)
 session.add(appointment8)
 session.add(appointment9)
 session.add(appointment10)
 session.commit()
 print("Appointments added")

 # 3.1
 askar = session.query(USER).filter_by(given_name='Askar', surname='Askarov').first()
 if askar:
     askar.phone_number = '+77771010001'
     session.commit()

 ed = session.query(USER).filter_by(given_name='Ed', surname='Sheeran').first()
 if ed:
     ed.phone_number = '+849862874'
     session.commit()

 print("3.1 Done")

 # 3.2
 caregivers_above_9 = session.query(CAREGIVER).filter(CAREGIVER.hourly_rate >= 9)
 for caregiver in caregivers_above_9:
     caregiver.hourly_rate *= 1.1
 caregivers_below_9 = session.query(CAREGIVER).filter(CAREGIVER.hourly_rate < 9)
 for caregiver in caregivers_below_9:
     caregiver.hourly_rate += 0.5
 session.commit()

 print("3.2 Done")

 # 4.1
 bolat_jobs_applications = (
     session.query(JOB_APPLICATION)
     .join(JOB, JOB_APPLICATION.job_id == JOB.job_id)
     .join(USER, JOB.member_user_id == USER.user_id)
     .filter(USER.given_name == 'Bolat', USER.surname == 'Bolatov')
 )
 for job_application in bolat_jobs_applications:
     session.delete(job_application)

 # Query and delete Bolat Bolatov's jobs
 bolat_jobs = (
     session.query(JOB)
     .join(USER, JOB.member_user_id == USER.user_id)
     .filter(USER.given_name == 'Bolat', USER.surname == 'Bolatov')
 )
 for job in bolat_jobs:
     session.delete(job)

 session.commit()

 print("4.1 Done")

 # 4.2
 turan_addresses = session.query(ADDRESS).join(MEMBER).filter(ADDRESS.street == 'Turan')
 turan_members = session.query(MEMBER).join(ADDRESS).filter(ADDRESS.street == 'Turan')
 for member in turan_addresses:
     session.delete(member)
     mem_id = member.member_user_id
     mem = session.query(MEMBER).filter(MEMBER.member_user_id == mem_id).first()
     session.delete(mem)
 session.commit()

 print("4.2 Done")

 # 5.1
 accepted_appointments = (
     session.query(APPOINTMENT, CAREGIVER, MEMBER)
     .join(CAREGIVER, APPOINTMENT.caregiver_user_id == CAREGIVER.caregiver_user_id)
     .join(MEMBER, APPOINTMENT.member_user_id == MEMBER.member_user_id)
     .filter(APPOINTMENT.status == 'Accepted')
     .all()
 )

 for appointment, caregiver, member in accepted_appointments:
     print(f"Appointment ID: {appointment.appointment_id}")
     print(f"Caregiver Name: {caregiver.given_name} {caregiver.surname}")
     print(f"Member Name: {member.given_name} {member.surname}")
     print("---")

 print("5.1 Done")

 # 5.2
 gentle_job_ids = (
     session.query(JOB.job_id)
     .filter(JOB.other_requirements.ilike('%gentle%'))
     .all()
 )

 if gentle_job_ids:
     job_ids_str = ', '.join(str(job_id[0]) for job_id in gentle_job_ids)
     print(f"Gentle Job IDs: {job_ids_str}")
 else:
     print("No jobs with 'gentle' in other requirements found.")

 print("5.2 Done")

 # 5.3
 baby_sitter_work_hours = (
     session.query(APPOINTMENT.work_hours)
     .join(CAREGIVER, APPOINTMENT.caregiver_user_id == CAREGIVER.caregiver_user_id)
     .join(JOB, APPOINTMENT.member_user_id == JOB.member_user_id)
     .filter(JOB.required_caregiving_type == 'Babysitter')
     .all()
 )

 if baby_sitter_work_hours:
     work_hours_list = [str(work_hour[0]) for work_hour in baby_sitter_work_hours]
     print(f"Babysitter Work Hours: {', '.join(work_hours_list)}")
 else:
     print("No babysitter appointments found.")

 print("5.3 Done")

 # 5.4
 elderly_care_members_query = (
     session.query(MEMBER)
     .join(JOB, MEMBER.member_user_id == JOB.member_user_id)
     .join(ADDRESS, MEMBER.member_user_id == ADDRESS.member_user_id)
     .filter(and_(JOB.required_caregiving_type == 'Elderly Care', ADDRESS.town == 'Astana', MEMBER.house_rules == 'No pets'))
 )

 elderly_care_members = elderly_care_members_query.all()
 elderly_care_member_names = [member.given_name for member in elderly_care_members]
 print(f"Members looking for Elderly Care in Astana with 'No pets.' rule: {elderly_care_member_names}")

 print("5.4 Done")

 # 6.1
 applicants_count_by_job = (
     session.query(JOB.job_id, func.count(JOB_APPLICATION.caregiver_user_id).label('applicants_count'))
     .outerjoin(JOB_APPLICATION, JOB.job_id == JOB_APPLICATION.job_id)
     .group_by(JOB.job_id)
     .all()
 )

 for job_id, count in applicants_count_by_job:
     print(f"Job ID {job_id}: {count} applicants")

 print("6.1 Done")

 # 6.2
 total_hours_spent = session.query(func.sum(APPOINTMENT.work_hours)).filter(APPOINTMENT.status == 'Accepted').scalar()
 print(f"Total hours spent by caregivers for all accepted appointments: {total_hours_spent} hours")

 print("6.2 Done")

 # 6.3
 average_pay = (
     session.query(func.avg(CAREGIVER.hourly_rate))
     .join(APPOINTMENT, CAREGIVER.caregiver_user_id == APPOINTMENT.caregiver_user_id)
     .filter(APPOINTMENT.status == 'Accepted')
     .scalar()
 )

 if average_pay is not None:
     print(f"Average pay of caregivers based on accepted appointments: ${average_pay:.2f} per hour")
 else:
     print("No accepted appointments or caregivers found.")

 print("6.3 Done")

 # 6.4 
 if average_pay is not None:
     above_average_earnings = (
         session.query(CAREGIVER)
         .join(APPOINTMENT, CAREGIVER.caregiver_user_id == APPOINTMENT.caregiver_user_id)
         .filter(APPOINTMENT.status == 'Accepted')
         .filter(CAREGIVER.hourly_rate > average_pay)
         .all()
     )
     above_average_caregiver_names = [caregiver.caregiver_user_id for caregiver in above_average_earnings]
     print(f"Caregivers who earn above average based on accepted appointments: {above_average_caregiver_names}")
 else:
     print("No accepted appointments or caregivers found.")

 print("6.4 Done")

 #7 
 total_cost = (
     session.query(func.sum(APPOINTMENT.work_hours * CAREGIVER.hourly_rate))
     .join(CAREGIVER, APPOINTMENT.caregiver_user_id == CAREGIVER.caregiver_user_id)
     .filter(APPOINTMENT.status == 'Accepted')
     .scalar()
 )
 if total_cost is not None:
     print(f"Total cost to pay for caregivers for all accepted appointments: ${total_cost:.2f}")
 else:
     print("No accepted appointments or caregivers found.")

 print("7 Done")

 # 8 
 job_applications = (
     session.query(JOB, JOB_APPLICATION, CAREGIVER)
     .join(JOB_APPLICATION, JOB.job_id == JOB_APPLICATION.job_id)
     .join(CAREGIVER, JOB_APPLICATION.caregiver_user_id == CAREGIVER.caregiver_user_id)
     .all()
 )
 for job, job_app, caregiver in job_applications:
     print(f"Job ID: {job.job_id}, Title: {job.required_caregiving_type}")
     print(f"Applicant: {caregiver.given_name} {caregiver.surname}, Caregiver ID: {caregiver.caregiver_user_id}")
     print(f"Application Date: {job_app.date_applied}")
     print("------")

 print("8 Done")

session.close()
engine.dispose()

