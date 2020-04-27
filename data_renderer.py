import pickle
import plotly.express as px
import pandas as pd

print('Twitch Data Renderer')
print('Enter a file name:')
f_name = input('> ')

with open(f_name + '.ttv', 'rb') as f:
    df = pickle.load(f)

bar_height = df['freq'].max()

fig = px.line(df, x='time', y='freq', hover_name='name', color='name')
# fig = px.bar(df, x='name', y='freq', animation_frame='time', color='name', range_y=[0, bar_height])
fig.show()
