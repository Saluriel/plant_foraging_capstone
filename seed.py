"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import db
from models import db, connect_db, User, PlantPin
from datetime import datetime


db.drop_all()
db.create_all()

u1 = User(id=1, username='username', password='password')
u2 = User(id=2, username='Linda', password='password')
u3 = User(id=3, username='Greg', password='password')
u4 = User(id=4, username='John', password='password')
u5 = User(id=5, username='Henry', password='password')
u6 = User(id=6, username='Elizabeth', password='password')
db.session.add_all([u1, u2, u3, u4, u5, u6])
db.session.commit()

p1 = PlantPin(user_id=1, date='datetime', plant = 'Mugwort', latitude = '43.50064471698356', longitude= '-84.96837234180853')
p2 = PlantPin(user_id=2, date='datetime', plant = 'Plant2', latitude = '42.50064483726196', longitude= '-84.96052537462853')
p3 = PlantPin(user_id=2, date='datetime', plant = 'Plant3', latitude = '43.53064471781936', longitude= '-84.98673534180853')
p4 = PlantPin(user_id=5, date='datetime', plant = 'Plant4', latitude = '43.10064471698356', longitude= '-84.96052593782853')
p5 = PlantPin(user_id=1, date='datetime', plant = 'Plant5', latitude = '43.50064443234656', longitude= '-84.02847534180853')
p6 = PlantPin(user_id=4, date='datetime', plant = 'Plant6', latitude = '43.50064478998748', longitude= '-84.36052534230853')
p7 = PlantPin(user_id=4, date='datetime', plant = 'Plant7', latitude = '41.50064471698356', longitude= '-84.96234534180853')
p8 = PlantPin(user_id=5, date='datetime', plant = 'Plant8', latitude = '40.50064471698356', longitude= '-84.96052583780853')
p9 = PlantPin(user_id=1, date='datetime', plant = 'Plant9', latitude = '41.50064471698356', longitude= '-84.78482534180853')
p10 = PlantPin(user_id=6, date='datetime', plant = 'Plant10', latitude = '43.50064121698356', longitude= '-84.9605223432253')
p11 = PlantPin(user_id=6, date='datetime', plant = 'Plant11', latitude = '43.50064471698356', longitude= '-84.9605928390853')
p12 = PlantPin(user_id=6, date='datetime', plant = 'Plant12', latitude = '43.54324471698356', longitude= '-84.2345677320853')
p13 = PlantPin(user_id=1, date='datetime', plant = 'Plant13', latitude = '43.50064471690286', longitude= '-84.96052523456853')

db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13])
db.session.commit()
