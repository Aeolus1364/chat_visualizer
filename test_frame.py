import pickle, pandas
import plotly.express as px
from collections import Counter

with open('hachu' + '.ttv', 'rb') as f:
    a = pickle.load(f)

df, counter = a 

sdf = pandas.DataFrame(counter.most_common(10))

fig = px.bar(sdf, x=0, y=1, color=0)
fig.show()