from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, ConnectionRefusedError, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
allow_origin_list = ['https://localhost', 'http://localhost', '127.0.0.1']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sender', methods=['POST'])
def sender():
    json = request.get_json(force=True)
    data = "%s" % (json)
    print(data)
    emit('my response', {'data': data}, namespace='/', broadcast=True)
    return jsonify({'msg': "Request sended to all clients connected"})

@socketio.on('my event')
def test_message(message):
    print(message)
    emit('my response', {'data': "Received"})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect')
def test_connect():
    if request.environ['REMOTE_ADDR'] in allow_origin_list:
        print('Client connected')
        emit('my response', {'data': 'Connected'})
    else:
        raise ConnectionRefusedError('unauthorized!')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)