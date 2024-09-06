from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, ConnectionRefusedError, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sender', methods=['GET'])
def sender():
    emit('my response', {'data': "Sended to clients"}, namespace='/', broadcast=True)
    return jsonify({'msg': "Request sended to all clients connected"})

@socketio.on('my event')
def test_message(message):
    print(message)
    emit('my response', {'data': "Received"})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect')
def test_connect(auth):
    if auth['X-My-Auth'] != "110168078":
        raise ConnectionRefusedError('unauthorized!')
    
    print('Client connected')
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)