import pandas as pd
import pickle
import plotly.express as px

def processor(df, master_counter, time_step, top_num=10):

    to_keep = [w[0] for w in master_counter.most_common(top_num)]
    
    # removes messages not in to_keep
    for i in df.iloc:
        name = i['name']
        if name not in to_keep:
            df = df[df.name != name]
            print(f'Removed {name}')

    # resets index numbers
    df = df.reset_index().drop(columns=['index'])

    print('Adding zeros...')
    unique_words = set(df['name'])
    max_time = df.iloc[-1]['time']

    # adds frequency 0 to times when messages have no data
    print(type(max_time), type(time_step))
    for t in range(0, int(max_time), int(time_step)):
        sliced_df = df.loc[df['time'] == t]
        for w in unique_words:
            names = sliced_df['name'].values
            if w not in names:
                df.loc[len(df)] = [w, t, 0]
                print(f'Added {w} at {t}')

    print('Done')

    print('Resorting...')
    df = df.sort_values(by=['time', 'name'])
    print('Done')
    return df

print('Twitch Data Processor')
print('Enter a file name:')
f_name = input('> ')

with open(f_name + '.raw', 'rb') as f:
    loaded = pickle.load(f)

df, master_counter, time_step = loaded
df_processed = processor(df, master_counter, time_step)

with open(f_name + '.ttv', 'wb') as f:
    pickle.dump(df_processed, f)