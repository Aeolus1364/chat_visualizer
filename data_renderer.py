import pickle
import plotly.express as px
import pandas as pd

def display_graph(df, counter, graph_type):
    bar_height = df['freq'].max()

    if graph_type == 'line':
        fig = px.line(df, x='time', y='freq', hover_name='name', color='name', range_y=[0, bar_height])
    elif graph_type == 'animated_bar':
        fig = px.bar(df, x='name', y='freq', animation_frame='time', color='name', range_y=[0, bar_height])
    elif graph_type == 'static_bar':
        fig = px.bar(df, x='name', y='freq')


    fig.show()


if __name__ == "__main__":
    print('Twitch Data Renderer')
    print('Enter a file name:')
    f_name = input('> ')

    with open(f_name + '.ttv', 'rb') as f:
        df = pickle.load(f)