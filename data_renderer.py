import pickle
import plotly.express as px
import pandas as pd

def display_graph(df, counter, graph_type):
    # calculates the maximum frequency to determine y range for graphs
    y_height = df['freq'].max()
    graph_ready = True

    # three different graph options
    if graph_type == 'line':
        fig = px.line(df, x='time', y='freq', hover_name='name', color='name', range_y=[0, y_height])
    elif graph_type == 'animated bar':
        fig = px.bar(df, x='name', y='freq', animation_frame='time', color='name', range_y=[0, y_height])
    elif graph_type == 'static bar':
        fig = px.bar(df, x='name', y='freq', color='name')
    else:
        graph_ready = False
    
    # doesn't try to show figure if invalid graph option entered
    if graph_ready:
        fig.show()

# following code only runs if you run data_renderer specifically
if __name__ == "__main__":
    print('Twitch Data Renderer')
    print('Enter a file name:')
    f_name = input('> ')

    print('Enter a graph type:')
    graph_type = input('> ')

    with open(f_name + '.ttv', 'rb') as f:
        df, counter = pickle.load(f)

    display_graph(df, counter, graph_type)
