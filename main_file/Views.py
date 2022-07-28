from flask import Blueprint,request,render_template
from flask_login import login_required,current_user
views  = Blueprint('views',__name__)

@views.route('/' , methods = ['GET','POST'])
@login_required
def home():
    name = request.form.get('name')
    messag = request.form.get('myMessage')
    return render_template('/index.html',name = current_user.username,messag=messag)

@views.route('/chat' , methods = ['GET' , 'POST'])
@login_required
def chat():
    return render_template('chat.html')