import pickle
import plotly.express as px

# reads token from external file to keep secret
with open("secret") as f: token = f.read().split("=")[1]

# User Input and Setup
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

# Data Collection
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

# Data Processing
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

print()
print('Starting data processing...')
processed_df = data_processor.processor(df, counter, ts)
save_data = processed_df, counter

print()
print('Saving data...')
with open(f_name + '.ttv', 'wb') as f:
    pickle.dump(save_data, f)
print('Done')

# Displaying Data
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

print()
print('Let\'s take a look at your data!')

while True:
    print('Type the following names to view graphs, or "quit" to quit:')
    print('"line" - simple line graph showing message count over time')
    print('"static bar" - bar graph showing most popular messages')
    print('"animated bar" - bar graph that animates message count every time step')
    graph_type = input('> ')
    if graph_type == 'quit':
        quit()
    data_renderer.display_graph(processed_df, counter, graph_type)
    print()