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
    html.H4('HCIL Deck', style={
        'textAlign': 'right',
        'color': colors['text']}),
    html.Img(src=app.get_asset_url('honda.png'), style={'textAlign': 'left', 'width': 80, 'height': 80}),
    html.Img(src=app.get_asset_url('ibm-security-logo.png'), style={'textAlign': 'left', 'width': 80, 'height': 80}),
    dcc.Tabs([
        dcc.Tab(label='Proxy Dashboard', children=[

            dcc.Dropdown(id='proxy-file-name',
                         options=[{'label': j.split('.c')[0], 'value': j}
                                  for j in pfiles],
                         value='',
                         multi=False,

                         ),

            html.Div(children=html.Div(id='graphs'), className='column'),

        ], className="container",
                style={'color': colors['text'], 'fontWeight': 'bold', 'backgroundColor': '#111111', 'width': '98%',
                       'margin-left': 10, 'margin-right': 10, 'max-width': 50000},
                selected_style={'color': colors['text'], 'fontWeight': 'bold', 'backgroundColor': '#111111'}
                )



        ], className='row', style={'color': colors['text'], 'backgroundColor': '#111111'},
                selected_style={'color': colors['text'], 'fontWeight': 'bold', 'backgroundColor': '#111111'}
                )])
], className="container", style={'width': '98%', 'margin-left': 10, 'margin-right': 10, 'max-width': 50000,
                                 'backgroundColor': colors['background']})


@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('proxy-file-name', 'value')])
def update_graph(pfile):

    df = pd.read_csv(pfile)
    cpu = df['CPU']
    ram = df['RAM']
    disk = df['Reporting/LoggingDisk']
    bdw = df['Average in last minute(Bandwidth)']
    txn = df['Average in last minute(Transactions per Second)']
    con = df['Current total server connections']
    times = df['TimeStamp']

    data1 = go.Scatter(
        x=times,
        y=cpu,
        mode='lines+markers',
        line=dict(color='#f77b23'))
    data2 = go.Scatter(
        x=times,
        y=ram,
        mode='lines+markers',
        line=dict(color='#f77b23'))
    data3 = go.Scatter(
        x=times,
        y=disk,
        mode='lines+markers',
        line=dict(color='#f77b23'))
    data4 = go.Scatter(
        x=times,
        y=bdw,
        mode='lines+markers',
        line=dict(color='#f77b23'))
    data5 = go.Scatter(
        x=times,
        y=txn,
        mode='lines+markers',
        line=dict(color='#f77b23'))
    data6 = go.Scatter(
        x=times,
        y=con,
        mode='lines+markers',
        line=dict(color='#f77b23'))

    graphs = [html.Div(dcc.Graph(
        id="data_name1",
        animate=False,
        figure={'data': [data1], 'layout': go.Layout(
            title='{}'.format('CPUU'),
            plot_bgcolor='#47260f',
            paper_bgcolor=colors['background'],
            font_color=colors['text']),
                })),
        html.Div(dcc.Graph(
            id="data_name2",
            animate=False,
            figure={'data': [data2], 'layout': go.Layout(
                title='{}'.format('RAM'),
                plot_bgcolor='#47260f',
                paper_bgcolor=colors['background'],
                font_color=colors['text']),
                    }, className='col s12 m6 l4')),
        html.Div(dcc.Graph(
            id="data_name3",
            animate=False,
            figure={'data': [data3], 'layout': go.Layout(
                title='{}'.format("DISK"),
                plot_bgcolor='#47260f',
                paper_bgcolor=colors['background'],
                font_color=colors['text']),
                    }, className='col s12 m6 l4')),
        html.Div(dcc.Graph(
            id="data_name4",
            animate=False,
            figure={'data': [data4], 'layout': go.Layout(
                title='{}'.format("Bandwidth"),
                plot_bgcolor='#47260f',
                paper_bgcolor=colors['background'],
                font_color=colors['text']),
                    }, className='col s12 m6 l4')),
        html.Div(dcc.Graph(
            id="data_name5",
            animate=False,
            figure={'data': [data5], 'layout': go.Layout(
                title='{}'.format('Transactions'),
                plot_bgcolor='#47260f',
                paper_bgcolor=colors['background'],
                font_color=colors['text']),
                    }, className='col s12 m6 l4')),
        html.Div(dcc.Graph(
            id="data_name6",
            animate=False,
            figure={'data': [data6], 'layout': go.Layout(
                title='{}'.format('Connections'),
                plot_bgcolor='#47260f',
                paper_bgcolor=colors['background'],
                font_color=colors['text']),
                    }, className='col s12 m6 l4'))
    ]
    return graphs


if __name__ == '__main__':
    app.run_server(debug=True)
