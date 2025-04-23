from arduino_iot_cloud import ArduinoCloudClient
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import threading
from datetime import datetime

# Arduino Cloud Configuration
DEVICE_ID = "448317bb-fb8d-454b-be1b-ed8af51e0448"
USERNAME = "448317bb-fb8d-454b-be1b-ed8af51e0448"
PASSWORD = "hfKWJm1ZJ#oX9iEZo#EeaFTL2"

# Thread-Safe Buffers
BUFFER_SIZE = 1000
data_lock = threading.Lock()
timestamps = deque(maxlen=BUFFER_SIZE)
x_data = deque(maxlen=BUFFER_SIZE)
y_data = deque(maxlen=BUFFER_SIZE)
z_data = deque(maxlen=BUFFER_SIZE)

# Dash App Initialization
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='graph-update', interval=100, n_intervals=0)  # 100ms updates
])

@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
def update_graph(n):
    with data_lock:
        ts = list(timestamps)   
        x = list(x_data)
        y = list(y_data)
        z = list(z_data)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts, y=x, name='X', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=ts, y=y, name='Y', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=ts, y=z, name='Z', line=dict(color='blue')))
    fig.update_layout(title='Real-Time Accelerometer Data', xaxis_title='Time', yaxis_title='Value')
    return fig

# Arduino Cloud Callbacks
def on_py_x(client, value):
    with data_lock:
        x_data.append(value)
        timestamps.append(datetime.now())

def on_py_y(client, value):
    with data_lock:
        y_data.append(value)

def on_py_z(client, value):
    with data_lock:
        z_data.append(value)

# Connect to Arduino Cloud
client = ArduinoCloudClient(device_id=DEVICE_ID, username=USERNAME, password=PASSWORD)
client.register("x_1", on_write=on_py_x)
client.register("y_1", on_write=on_py_y)
client.register("z_1", on_write=on_py_z)

# Start Threads
cloud_thread = threading.Thread(target=client.start)    
cloud_thread.daemon = True
cloud_thread.start()

if __name__ == '__main__':
    app.run_server(debug=False)