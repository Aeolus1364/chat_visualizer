import socket, time, math, pickle
from collections import Counter
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

SERVER = 'irc.chat.twitch.tv'
PORT = 6667
NICKNAME = 'chat_visualizer'

# reads token from external file to keep secret
with open("secret") as f: token = f.read().split("=")[1]

def twitch_reader(channel, time_step, max_time=0, max_msg=0):
    channel = '#' + channel

    sock = socket.socket()
    sock.connect((SERVER, PORT))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {NICKNAME}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    
    # ignores server join messages
    sock.recv(2048)
    sock.recv(2048)
    sock.recv(2048)

    steps_taken = 0
    msg_count = 0

    df = pd.DataFrame(columns=['name', 'time', 'freq'])

    initial_time = time.time()
    active_counter = Counter()
    master_counter = Counter()
    
    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')
            elapsed_time = time.time() - initial_time
            
            # backend message to keep connection alive
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))

            else:
                raw_msg = resp.splitlines()
                for line in raw_msg:
                    msg = line.split()
                    # this line is a little confusing, but all it does is remove the ':' from the beginning of the first word 
                    # it is then cast to set to remove duplicate entries
                    try:
                        words = set([msg[3][1:]] + msg[4:])
                    except IndexError:
                        print('error')
                        print(line, words)
                        break

                    print(words)
                    # print(raw_msg.splitlines())

                    # adds words from current message to the current time step's Counter
                    active_counter.update(words)
                    master_counter.update(words)

                    # calculates how many steps should exist at the current time
                    # and generates empty steps if no messages are sent over a long time period
                    ideal_steps = math.floor(elapsed_time / time_step)
                    new_steps = ideal_steps - steps_taken
                    for s in range(new_steps):
                        for i in active_counter:
                            name = i
                            freq = active_counter[i]

                            # calculates elapsed time from num steps taken and step length
                            step = steps_taken * time_step

                            # continuously appends new rows to the end of the dataframe
                            # print(name, step, freq)
                            df.loc[len(df)] = [name, step, freq]
                

                        active_counter = Counter()
                        steps_taken += 1
                    
                    # print(df)
            msg_count += 1
        
            if max_msg and msg_count > max_msg:
                break
            if max_time and elapsed_time > max_time:
                break

    except KeyboardInterrupt:
        pass

    # for r in range(1):
    #     for w in unique_words:
    #         row = df.iloc[r]
    #         if w in row['name']:
    #             print(row)

    return df, master_counter


# print('Twitch Data Collector')
# print('Enter a file name:')
# f_name = input('> ')

# print('Enter a channel name:')
# channel = input('> ')

# while True:
#     print('Enter a collection time in seconds:')
#     print('(or enter 0 for no limit, cancel with Ctrl + C)')
#     try:
#         length = float(input('> '))
#     except ValueError:
#         continue
#     break

# while True:
#     print('Enter a sample time in seconds:')
#     try:
#         sample_time = float(input('> '))
#     except ValueError:
#         continue
#     break

# data = twitch_reader(channel, sample_time, max_time=length)

data = twitch_reader('xqcow', 5, 60)
f_name = 'xqc'
with open(f_name + '.ttv', 'wb') as f:
    pickle.dump(data, f)
