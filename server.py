import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    print()

@sio.event
def my_message(sid, data):
    print('message ', data)
    print()

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    print()

@sio.on('send')
def send(sid, data):
    print('send message ', data)
    sio.emit('receive', str(data), skip_sid=sid)

if __name__ == '__main__':
    ip = input('Set IP Address: ')
    port = input('Set Port: ')
    eventlet.wsgi.server(eventlet.listen((str(ip), int(port))), app)