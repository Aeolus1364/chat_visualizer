import pickle
import plotly.express as px
import pandas as pd

# print('Twitch Data Renderer')
# print('Enter a file name:')
# f_name = input('> ')
f_name = 'xqc'


with open(f_name + '.ttv', 'rb') as f:
    loaded = pickle.load(f)

df, master_counter = loaded
print(df.iloc[len(df) - 1]['time'])
# print(master_counter)

unique_words = set(df['name'])

# for n in df['time']:
#     print(n)
    # for w in unique_words:
    # print(n)

# fig = px.line(df, x='time', y='freq', hover_name='name', color='name')
# # fig = px.bar(df, x='name', y='freq', animation_frame='time', color='name')
# fig.show()
