import pandas as pd
from datetime import datetime, timedelta
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import glob

print('start')





external_css = ["https://codepen.io/anon/pen/mardKv.css"]
app = dash.Dash(__name__,external_stylesheets=external_css)
server = app.server
app.title = 'HCIL Deck'


theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}
path = r'C:\Users\AdityaKumar\Desktop\Honda_Proxy_Automation\Raw_data\\'

df = pd.read_csv('10.117.22.37_03052020.csv')




cpu = df['CPU']
ram = df['RAM']
disk = df['Reporting/LoggingDisk']
bdw = df['Average in last minute(Bandwidth)']
txn = df['Average in last minute(Transactions per Second)']
con = df['Current total server connections']
times = df['TimeStamp'  ]


from datetime import datetime as dt

data_dict = {"CPU": cpu,
             "RAM": ram,
             "DISK": disk,
             "Bandwidth": bdw,
             "Transactions": txn,
             "Connections": con}

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}






app.layout = html.Div([
    html.H4('HCIL Deck',style={
        'textAlign': 'right',
        'color': colors['text']}),
    html.Img(src=app.get_asset_url('honda.png'),style={'textAlign': 'left','width':80,'height':80}),
    html.Img(src=app.get_asset_url('ibm-security-logo.png'),style={'textAlign': 'left','width':80,'height':80}),
    dcc.Tabs([
        dcc.Tab(label='Proxy Dashboard', children=[
             
             
             dcc.Dropdown(id='proxy-data-name',
                         options=[{'label': s, 'value': s}
                                  for s in data_dict.keys()],
                         value='',
                         multi=True,
                         
                         ),
             html.Div(children=html.Div(id='graphs'), className='row')
            
        ], className="container", style={'color':colors['text'],'fontWeight': 'bold','backgroundColor': '#111111','width': '98%', 'margin-left': 10, 'margin-right': 10, 'max-width': 50000},
           selected_style={'color':colors['text'],'fontWeight': 'bold','backgroundColor': '#111111'}  
        )
        
    ])
],style={'backgroundColor': colors['background']})



@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('proxy-data-name', 'value')])


def update_graph(data_names):
    graphs = []

    for data_name in data_names:
        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            mode='lines+markers'
        )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data], 'layout': go.Layout(
                margin={'l': 50, 'r': 1, 't': 45, 'b': 1},
                title='{}'.format(data_name),
                plot_bgcolor='#DCDCDC')}
        ), className='col s12 m6 l6'))
        return  graphs

if __name__ == '__main__':
    app.run_server(debug=True)
