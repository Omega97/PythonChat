"""
Client-side code
connect and send messages to server
"""
import socketio


# global parameters
sio = socketio.Client()


def input_non_empty(header=''):
    s = ''
    while not s:
        s = input(header)
    return s


def send_messages_to_server():
    """send messages to server"""
    while True:
        try:
            text = input_non_empty()
            sio.emit('message', {'text': text})
        except KeyboardInterrupt:
            break
    sio.disconnect()
    print("> Disconnected")


def connect_to_server():
    """
    try to connect to server
    :return: True if connection successful, else False
    """
    print('> Connecting to chat...')
    try:
        # sio.connect('http://localhost:8080/')
        sio.connect('http://146.241.54.49:8080/')

    except Exception as e:
        print(f'> Could not connect to server ({e})')
        return False
    print('> Connected\n')
    return True


def choose_nickname():
    """choose a nickname that is not already taken"""
    nickname = input_non_empty('nickname: ')
    sio.emit('set nickname', {'nickname': nickname})
    print('> Chat ready')


# ---------- @sio.on methods ----------


@sio.event
def message(data):
    """receive from server"""
    print(f'>{data["nickname"]}: {data["text"]}')


# ----------  ----------


def main():
    """connect to server with username"""
    if not connect_to_server():
        return
    choose_nickname()
    send_messages_to_server()


if __name__ == "__main__":
    main()
