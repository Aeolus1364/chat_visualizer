import socket, time, math, pickle
from collections import Counter
import pandas as pd

def twitch_reader(token, channel, time_step, max_time=0, max_msg=0, remove_duplicates=True, SERVER='irc.chat.twitch.tv', PORT=6667, NICKNAME='chat_visualizer'):
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
            try:
                resp = sock.recv(2048).decode('utf-8')
            except UnicodeDecodeError:
                print('Unicode Decode Error')
                continue

            elapsed_time = time.time() - initial_time
            
            # backend message to keep connection alive
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))

            else:
                # if chat is high volume, messages sent together and need to be split by line
                raw_msg = resp.splitlines()
                for line in raw_msg:
                    # for each line, the message is extracted and sent to words list
                    msg = line.split()
                    words = []
                    msg_begin = False
                    for w in msg:
                        if msg_begin:
                            words.append(w)
                        if w == channel:
                            msg_begin = True

                    if words:
                        # removes ':' from beginning of first word
                        words[0] = words[0][1:]
                    
                    # prints out messages for viewing
                    print(' '.join(words))

                    if remove_duplicates:
                        # casting words to a set removes duplicate entries
                        words = set(words)
                            
                    # print(words)

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
                    
            msg_count += 1
        
            if max_msg and msg_count > max_msg:
                break
            if max_time and elapsed_time > max_time:
                break

    except KeyboardInterrupt:
        pass

    return df, master_counter, time_step

if __name__ == "__main__":
    # reads token from external file to keep secret
    with open("secret") as f: token = f.read().split("=")[1]

    print('Twitch Data Collector')
    print('Enter a file name:')
    f_name = input('> ')

    print('Enter a channel name:')
    channel = input('> ')

    while True:
        print('Enter a collection time in seconds:')
        print('(or enter 0 for no limit, cancel with Ctrl + C)')
        try:
            length = int(input('> '))
        except ValueError:
            continue
        break

    while True:
        print('Enter a sample time in seconds:')
        try:
            sample_time = int(input('> '))
        except ValueError:
            continue
        break

    print('Beginning collection...')

    data = twitch_reader(token, channel, sample_time, max_time=length)

    # saves collected data to a .raw file, unprocessed data
    with open(f_name + '.raw', 'wb') as f:
        pickle.dump(data, f)