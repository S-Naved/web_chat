from pprint import pprint
from flask import Flask, render_template,request
from flask_socketio import send,SocketIO,emit

app = Flask(__name__)
app.config['SECRET_KEY']='sdasdas'
socket = SocketIO(app,logger=True, engineio_logger=True)

all_msg = {
    'user_name':'',
    'message':''
}

@app.route('/' , methods = ['GET','POST'])
def home():
    return render_template('/index.html')

@socket.on_error_default
def error_handler(e):
    print('An error occured :'+str(e))

@socket.on('my envet')
def handle_message(data , mehtods=['GET','POST']):
    print('Message: ' + str(data) )
    user = data['user_name']
    msgs = data['message']
    # image = data['image']
    # if not image:
    #     print('please select image')
    # print(type(image))
    print(f'username:-{user} \n message:-{msgs}  \n user_sid:{request.sid}')
    emit('my response',data,broadcast = True)
    

if __name__ == '__main__':
    # app.run()
    socket.run(app ,debug = True)