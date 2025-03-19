import dash
from dash import dcc, html, Input, Output, State, dash_table  # This is the import statement
import plotly.express as px
import pandas as pd


df = pd.read_csv('gyroscope_data.csv') #This will load the csv file 


app = dash.Dash(__name__) # This will initialize the Dash app

# This is Layout of the app
app.layout = html.Div([
    html.H1("Gyroscope Data Visualization"),
    
    # here we can select the graph type
    html.Label("Select Graph Type:"),
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Distribution Plot', 'value': 'histogram'}
        ],
        value='line'
    ),
    
    # Dropdown to select data variables
    html.Label("Select Data Variables:"),
    dcc.Dropdown(
        id='data-vars',
        options=[
            {'label': 'X', 'value': 'x'},
            {'label': 'Y', 'value': 'y'},
            {'label': 'Z', 'value': 'z'},
            {'label': 'All', 'value': 'all'}
        ],
        value='all',
        multi=True
    ),
    
    # Text box to input number of samples
    html.Label("Number of Samples:"),
    dcc.Input(id='sample-size', type='number', value=10),
    
    # Navigation buttons
    html.Button('Previous', id='prev-button', n_clicks=0),
    html.Button('Next', id='next-button', n_clicks=0),
    
    # Graph
    dcc.Graph(id='gyro-graph'),
    
    # Table to summarize data
    html.Label("Data Summary:"),
    dash_table.DataTable(  # Updated usage of dash_table
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )
])

# Callback to update graph and table based on user input
@app.callback(
    [Output('gyro-graph', 'figure'),
     Output('data-table', 'data')],
    [Input('graph-type', 'value'),
     Input('data-vars', 'value'),
     Input('sample-size', 'value'),
     Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks')],
    [State('gyro-graph', 'figure')]
)
def update_graph(graph_type, data_vars, sample_size, prev_clicks, next_clicks, current_figure):
    # Determine the start index based on navigation buttons
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'prev-button':
        start_idx = max(0, prev_clicks * sample_size)
    elif button_id == 'next-button':
        start_idx = next_clicks * sample_size
    else:
        start_idx = 0
    
    end_idx = start_idx + sample_size
    df_subset = df.iloc[start_idx:end_idx]
    
    # Select data variables
    if data_vars == 'all':
        selected_vars = ['x', 'y', 'z']
    else:
        selected_vars = data_vars if isinstance(data_vars, list) else [data_vars]
    
    # Create the graph based on the selected type
    if graph_type == 'scatter':
        fig = px.scatter(df_subset, x='timestamp', y=selected_vars, title='Scatter Plot of Gyroscope Data')
    elif graph_type == 'line':
        fig = px.line(df_subset, x='timestamp', y=selected_vars, title='Line Chart of Gyroscope Data')
    elif graph_type == 'histogram':
        fig = px.histogram(df_subset, x=selected_vars, title='Distribution Plot of Gyroscope Data')
    
    # Update the table with the current data subset
    table_data = df_subset.to_dict('records')
    return fig, table_data
if __name__ == '__main__':    # This final step runs the app
    app.run_server(debug=True)