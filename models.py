from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""

    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    location = db.Column(db.Text)

    pins = db.relationship("PlantPin")

    @classmethod
    def signup(cls, username, email, password, location):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            location=location,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
        
class PlantPin(db.Model):
    """Model for the pins to show where plants are located"""

    __tablename__="plant_pins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    date = db.Column(db.Text, nullable=False)
    plant = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Text, nullable=False)
    longitude = db.Column(db.Text, nullable=False)

    def serialize(self):
        s = Serializer.serialize(self)
        del s['id']
        return s



class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
    