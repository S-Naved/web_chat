from flask import Flask, render_template,request,session
from flask_socketio import send,SocketIO,emit

app = Flask(__name__)
app.config['SECRET_KEY']='sdasdas'
socket = SocketIO(app,logger=True, engineio_logger=True)

all_users =[]

@app.route('/' , methods = ['GET','POST'])
def home():
    name = request.form.get('name')
    messag = request.form.get('myMessage')
    print(f'this is all users{all_users}')
    return render_template('/index.html',name = name,messag=messag)

@socket.on_error_default
def error_handler(e):
    print('An error occured :'+str(e))

@socket.on('my envet')
def handle_message(data , mehtods=['GET','POST']):
    print('Message: ' + str(data) )
    user = data['user_name']
    room = [all_users[0]['user_id'],all_users[1]['user_id']]

    msgs = data['message']
    # image = data['image']
    # if not image:
    #     print('please select image')
    # print(type(image))
    data1 = {'user_sid':request.sid}
    new_data = {**data,**data1}
    if request.sid in room:
        user_room = session.get('room')
        print(f'username:-{user} \n message:-{msgs}  \n user_sid:{request.sid} \n userroom:{user_room}')
        emit('my response',new_data,broadcast = True , to =room) 
    else:
        common_room = all_users[2::]
        print('0000000000000000000000000000000000000000000000000000000')
        cmn_rm  =[n['user_id'] for n in common_room]
        emit('my response',new_data,broadcast = True , to =cmn_rm)

@socket.on('private')
def private_msg(msg):
    
    pass

@socket.on('connect')
def test_connect( mehtods=['GET','POST']):
    all_users.append({'user_id':request.sid})
    print('-------------------------------------------------')
    print(all_users)
    print('-------------------------------------------------')
    emit('my response', {'data': 'Connected','user_sid':request.sid})
dis = []
@socket.on('disconnect')
def test_disconnect():
    print('-------------------------------------------------')
    print(f'user disconnect id is:{request.sid}')
    all_users.remove({'user_id':request.sid})
    dis.append(request.sid)
    print('-------------------------------------------------')
    print('Client disconnected')
    print(f'all disconnected users{dis}')


if __name__ == '__main__':
    # app.run()
    socket.run(app ,debug = True)