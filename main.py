import pickle
import plotly.express as px

# reads token from external file to keep secret
with open("secret") as f: token = f.read().split("=")[1]

print('Welcome to Twitch Chat Analysis!')

print()
print('To get started, please enter a twitch channel')
print('This can be found at the end of their url:')
print('https://www.twitch.tv/?????')
channel = input('> ')

while True:
        print()
        print('Now enter how many seconds you want to collect data for')
        print('Or enter 0 if you don\'t want to set a limit')
        print('You can stop recording at any time by pressing Ctrl + C')
        try:
            time_limit = int(input('> '))
        except ValueError:
            continue
        break

while True:
        print()
        print('Next enter how many seconds each "time step" should be')
        print('This will determine the resolution of the data')
        print('(Recommended 5 seconds)')
        try:
            time_step = int(input('> '))
        except ValueError:
            continue
        break

print()
print('Finally, enter a file name to save your data')
print('A .raw and .ttv file will be generated')
f_name = input('> ')

print()
print('Let\'s get started!')

print('Importing data collector...')
import data_collector
print('Done')

print()
print('Importing data processor...')
import data_processor
print('Done')

print()
print('Importing data renderer...')
import data_renderer
print('Done')


print()
print('Starting data collection...')
print()

data = data_collector.twitch_reader(token, channel, time_step, max_time=time_limit, remove_duplicates=False)
df, counter, ts = data
print('Collection complete!')

print()
print('Saving data...')
with open(f_name + '.raw', 'wb') as f:
    pickle.dump(data, f)
print('Done')

print()
print('Starting data processing...')
processed_df = data_processor.processor(df, counter, ts)
save_data = processed_df, counter

print()
print('Saving data...')
with open(f_name + '.ttv', 'wb') as f:
    pickle.dump(save_data, f)
print('Done')

print()
print('Let\'s take a look at your data!')

print('Type "bar" or "line" to view graphs')
graph_type = input('> ')

bar_height = processed_df['freq'].max()
if graph_type == 'bar':
    fig = px.bar(processed_df, x='name', y='freq', animation_frame='time', color='name', range_y=[0, bar_height])
elif graph_type == 'line':
    fig = px.line(processed_df, x='time', y='freq', hover_name='name', color='name', range_y=[0, bar_height])

fig.show()
