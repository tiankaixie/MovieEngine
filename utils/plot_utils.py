import plotly.plotly as py
import plotly.graph_objs as go

def plot_heatmap(X):
	data = [go.Heatmap(z = X)]
	py.iplot(data, filename='features-heatmap')