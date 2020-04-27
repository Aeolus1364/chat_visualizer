import socket, select

with open("secret") as f: token = f.read().split("=")[1]
SERVER='irc.chat.twitch.tv'
PORT=6667
NICKNAME='chat_visualizer'
channel = '#hasaabi'



sock = socket.socket()
sock.connect((SERVER, PORT))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {NICKNAME}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

ready = select.select([sock], [], [], 5)
if ready[0]:




    # ignores server join messages

    sock.recv(2048)
    sock.recv(2048)
    sock.recv(2048)

while True:
    try:
        resp = sock.recv(2048).decode('utf-8')
    except UnicodeDecodeError:
        print('Unicode Decode Error')
        continue

    print(resp)
    # backend message to keep connection alive
    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
