"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import db
from models import db, connect_db, User, Plant, PlantPin


db.drop_all()
db.create_all()



db.session.commit()
