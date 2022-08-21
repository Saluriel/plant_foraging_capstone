"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import db
from models import db, connect_db, User, Plant, PlantPin
from datetime import datetime


db.drop_all()
db.create_all()

u1 = User(id=1, username='username', password='password')
db.session.add(u1)
db.session.commit()

p1 = PlantPin(user_id=1, date='datetime', plant = 'Mugwort', latitude = '8', longitude= '8')
p2 = PlantPin(user_id=1, date='datetime', plant = 'Plant2', latitude = '8', longitude= '8')
p3 = PlantPin(user_id=1, date='datetime', plant = 'Plant3', latitude = '8', longitude= '8')
p4 = PlantPin(user_id=1, date='datetime', plant = 'Plant4', latitude = '8', longitude= '8')

db.session.add_all([p1, p2, p3, p4])
db.session.commit()
