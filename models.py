from extentions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    nickname = db.Column(db.String(100))
    type = db.Column(db.String(3), nullable=False)  # usr-user cpn-company cbr-chamber
    comp_id = db.Column(db.Integer)
    cham_id = db.Column(db.Integer)
    signup_time = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'nickname': self.nickname,
            'type': self.type,
            'comp_id': self.comp_id,
            'cham_id': self.cham_id,
            'signup_time': self.signup_time
        }


class CollectionCompany(db.Model):
    __tablename__ = "collection_company"
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    comp_id = db.Column(db.Integer, primary_key=True, nullable=False)
    collect_time = db.Column(db.DateTime, default=datetime.now())


class CollectionChamber(db.Model):
    __tablename__ = "collection_chamber"
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    cham_id = db.Column(db.Integer, primary_key=True, nullable=False)
    collect_time = db.Column(db.DateTime, default=datetime.now())


class Company(db.Model):
    __tablename__ = "company"
    comp_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    cham_id = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(100), nullable=False)
    wechat = db.Column(db.String(50))
    link = db.Column(db.String(200))
    intro = db.Column(db.String(200))
    signup_time = db.Column(db.DateTime, default=datetime.now())


class Chamber(db.Model):
    __tablename__ = "chamber"
    cham_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(100), nullable=False)
    wechat = db.Column(db.String(50))
    link = db.Column(db.String(200))
    intro = db.Column(db.String(200))
    signup_time = db.Column(db.DateTime, default=datetime.now())


class Rating(db.Model):
    __tablename__ = "rating"
    rid = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    cham_id = db.Column(db.Integer)
    comp_id = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now())
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000))

