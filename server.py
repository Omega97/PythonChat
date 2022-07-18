"""
Server-side code
handling client connection, receive messages from client
"""
import socketio
from aiohttp import web
from datetime import datetime


# global parameters
sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)
member_nicknames = dict()   # {user_id: nickname}


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def pprint(text):
    """print text in special format"""
    print(f'> [{now()}] {text}')


# ---------- @sio.on methods ----------


@sio.event
async def message(user_id, data):
    """receive message from client"""
    nickname = member_nicknames[user_id]
    pprint(f'{nickname}: {data["text"]}')
    data = {'text': data["text"],
            'nickname': member_nicknames[user_id]}
    await sio.emit('message', data, broadcast=True, skip_sid=user_id)


@sio.event
def connect(user_id, *_):
    """ standard, connect client to server """
    pprint(f'Beginning transmission (id={user_id})')


@sio.event
def disconnect(user_id):
    """
    standard, disconnect client from server
    :param user_id: hash of client
    """
    if user_id in member_nicknames:
        nickname = member_nicknames[user_id]
        member_nicknames.pop(user_id)
        pprint(f'{nickname} left the chat')


@sio.on('set nickname')
def set_nickname(user_id, data):
    """
    standard, connect client to server
    :param user_id: hash of client
    :param data: dict, contains user nickname
    """
    nickname = data["nickname"]
    member_nicknames[user_id] = nickname
    pprint(f'{nickname} joined the chat')


# ----------  ----------


def main():
    """start and run server"""
    pprint("Starting server...")
    web.run_app(app, port=80)


if __name__ == "__main__":
    main()
