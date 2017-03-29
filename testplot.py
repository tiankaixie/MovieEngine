import matplotlib.pyplot as plt
from scipy.io import loadmat
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np

x0 = np.random.randn(500)
x1 = np.random.randn(500)+1

trace1 = go.Histogram(
    x=x0,
    opacity=0.75
)
trace2 = go.Histogram(
    x=x1,
    opacity=0.75
)

data = [trace1, trace2]
layout = go.Layout(barmode='overlay')
fig = go.Figure(data=data, layout=layout)

py.iplot(fig, filename='overlaid histogram')