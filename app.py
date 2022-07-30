from datetime import datetime
from flask import Flask, render_template,request,session
from flask_socketio import send,SocketIO,emit,join_room
from sqlalchemy import or_
from main_file import create_app,db
from main_file.model import User,Room
from flask_login import current_user
app = create_app()
socket = SocketIO(app,logger=True, engineio_logger=True)

all_users =[]


@socket.on_error_default
def error_handler(e):
    print('An error occured :'+str(e))

@socket.on('my envet')
def handle_message(data , mehtods=['GET','POST']):
    print('Message: ' + str(data) )
    msgs = data['message']
    user_name = data['name']
    s_public_id = data['public_id']
    o_public_id = data['user_public_id']
    room_1 = s_public_id + o_public_id
    room_2 = o_public_id + s_public_id
    user_room1 = Room.query.filter_by(room_name = room_1).first()
    user_room2 = Room.query.filter_by(room_name = room_2).first()
    sender_user = User.query.filter_by(public_id = s_public_id).first()
    reciver_user = User.query.filter_by(public_id = o_public_id).first()
    
    if user_room1:
        old_data = user_room1.chat_msgs
        new_data = []
        new_dic = {
            'username':user_name,
            'msg':msgs
        }
        new_data.append(new_dic)
            
        if old_data:
            user_room1.chat_msgs = old_data + new_data
            db.session.add(user_room1) 
        else:
            user_room1.chat_msgs = new_dic
            db.session.add(user_room1)
        db.session.commit()
        if reciver_user.user_status:
            join_room(room_1)
            emit('my response',data , room = room_1)
        else:
            join_room(room_1)
            emit('my response',data , room = room_1)
            print('push notification')
    elif user_room2:
        old_data = user_room2.chat_msgs
        new_data2 = []
        new_dic2 = {
            'username':user_name,
            'msg':msgs
        }
        new_data2.append(new_dic2)
            
        if old_data:
            user_room2.chat_msgs = old_data + new_data2
            db.session.add(user_room2) 
        else:
            user_room2.chat_msgs = new_data2
            db.session.add(user_room2)
        db.session.commit()
        if reciver_user.user_status:
            join_room(room_2)
            emit('my response',data , room = room_2)
        else:
            join_room(room_2)
            emit('my response',data , room = room_2)
            print('push notification')
        
    else:
        first_msg = []
        first_msg_dic = {
            'username':user_name,
            'msg':msgs
        }
        first_msg.append(first_msg_dic)
        if not sender_user.id == reciver_user.id:
            add_room = Room (user_1 = sender_user.id , user_2 = reciver_user.id ,
                            room_name = room_1 , chat_msgs = first_msg, chat_msg_t =
                            first_msg , date_create = datetime.now())
            
            db.session.add(add_room)
            db.session.commit()
        if reciver_user.user_status:
            join_room(room_1)
            emit('my response',data , room = room_1)
        else:
            join_room(room_1)
            emit('my response',data , room = room_1)
            print('push notification')

@socket.on('joins')
def on_join(data):
    """User joins a room"""

    username = data["username"]
    room = data["room"]
    join_room(room)

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room + " room."}, room=room) 

@socket.on('roommsg')
def roommsg(data , mehtods=['GET','POST']):
    msg = data['message']
    username = data['username']
    room  = data['room']
    print('//////////////////////////////////////////////////')
    print(msg)
    print(username)
    print(room)
    print('//////////////////////////////////////////////////')
    emit('my room',data,room = room)




@app.route('/demo' , methods = ['GET','POST'])
def demo():
    appuser = User.query.filter_by(id = current_user.id).first()
    roomdata = Room.query.filter(or_(Room.user_1 == appuser.id,
                                    Room.user_2 == appuser.id)).first()
    return render_template('demo.html', name = current_user , roomdata = roomdata)

@socket.on('join')
def private_msg(data):
    s_public_id = data['public_id']
    o_public_id = data['user_public_id']
    room_1 = s_public_id + o_public_id
    room_2 = o_public_id + s_public_id
    user_room1 = Room.query.filter_by(room_name = room_1).first()
    user_room2 = Room.query.filter_by(room_name = room_2).first()
    sender_user = User.query.filter_by(public_id = s_public_id).first()
    reciver_user = User.query.filter_by(public_id = o_public_id).first()
    
    # join_room(data[room])
    pass

@socket.on('connect')
def test_connect( mehtods=['GET','POST']):
    
    print('-------------------------------------------------')
    print(current_user.id)
    current_user.user_status = True
    db.session.commit()
    current_user.sock_id = request.sid
    db.session.commit()
    # 
    user_room = Room.query.filter(or_(Room.user_1 == current_user.id ,Room.user_2 == current_user.id )).all()
    for rooms in user_room:

        join_room(rooms.room_name)
        print(f'user has join {rooms.room_name}')
    print('-------------------------------------------------')
    emit('my response', {'data': 'Connected','user_sid':request.sid,'user_id':current_user.id
                    ,'username':current_user.username})
dis = []
@socket.on('disconnect')
def test_disconnect():
    print('-------------------------------------------------')
    print(f'user disconnect id is:{request.sid}')
    print(current_user.id)
    current_user.user_status = False
    db.session.commit()
    print('-------------------------------------------------')
    print('Client disconnected')
    

if __name__ == '__main__':
    # app.run()
    socket.run(app ,debug = True)