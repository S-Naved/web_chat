from flask import Blueprint,request,render_template
from flask_login import login_required,current_user
from sqlalchemy import or_ 
from .model import Room, User
views  = Blueprint('views',__name__)

@views.route('/' , methods = ['GET','POST'])
@login_required
def home():
    appuser = User.query.filter_by(id = current_user.id).first()
    user_room = Room.query.filter(or_(Room.user_1 == appuser.id ,Room.user_2 == appuser.id )).all()
    return render_template('/index.html',name = current_user.username,user_room = user_room)


@views.route('/chat' , methods = ['GET' , 'POST'])
@login_required
def chat():
    appuser = User.query.filter_by(id = current_user.id).first()
    user_room = Room.query.filter(or_(Room.user_1 == appuser.id ,Room.user_2 == appuser.id )).all()
    return render_template('chat.html',name = current_user.username)