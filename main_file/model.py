from . import db
from flask_login import UserMixin


class User(db.Model,UserMixin):
    __tablename__ = 'appusers'
    id          =  db.Column(db.Integer,primary_key = True)
    email       =  db.Column(db.String(150),unique = True)
    username    =  db.Column(db.String(150),unique = True)
    password    =  db.Column(db.String(150))
    user_status =  db.Column(db.Boolean(), default = False)
    profile_pic =  db.Column(db.String(600),nullable = True,
                      default='persondefault_profile.png')
    date_created= db.Column(db.DateTime ) 
    date_create = db.Column(db.DateTime )

class Room(db.Model):
    __tablename__= 'rooms'
    id = db.Column(db.Integer , primary_key = True)
    user_1 = db.Column(db.Integer , nullable = True)
    user_2 = db.Column(db.Integer , nullable = True)
    room_id = db.Column(db.String(700), nullable = True)
    chat_msgs = db.Column(db.JSON() , nullable = True)
    chat_msg_t = db.Column(db.Text , nullable = True)
    date_create = db.Column(db.DateTime )