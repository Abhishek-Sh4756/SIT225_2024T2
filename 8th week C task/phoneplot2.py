import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import threading
from datetime import datetime

def create_realtime_dashboard(
    title="Real-Time Data",
    streams=["Data"],
    buffer_size=1000,
    update_interval=100,
    line_colors=None,
    yaxis_title="Value",
    xaxis_title="Time"
):
   
    
    # Initialize data structures
    data_lock = threading.Lock()
    timestamps = deque(maxlen=buffer_size)
    data_buffers = {name: deque(maxlen=buffer_size) for name in streams}
    
    # Set default colors if not provided
    if line_colors is None:
        colors = ['red', 'green', 'blue', 'purple', 'orange']
        line_colors = {name: colors[i % len(colors)] for i, name in enumerate(streams)}
    
    # Create Dash app
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        dcc.Graph(id='live-graph'),
        dcc.Interval(
            id='graph-update',
            interval=update_interval,
            n_intervals=0
        )
    ])
    
    @app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
    def update_graph(n):
        with data_lock:
            ts = list(timestamps)
            current_data = {name: list(buffer) for name, buffer in data_buffers.items()}
        
        fig = go.Figure()
        for name in streams:
            fig.add_trace(go.Scatter(
                x=ts,
                y=current_data[name],
                name=name,
                line=dict(color=line_colors[name])
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title
        )
        return fig
    
    def push_data(**kwargs):
        """Push new data values to the dashboard"""
        with data_lock:
            for name, value in kwargs.items():
                if name in data_buffers:
                    data_buffers[name].append(value)
            timestamps.append(datetime.now())
    
    return app, push_data