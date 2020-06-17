import pandas as pd
from datetime import datetime, timedelta
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import glob

print('start')

def symantec_data():
    os.chdir(r'c:\Users\AdityaKumar\Desktop\Honda_symantec_automation\raw_dump')
    files = glob.glob('*.csv')
    files.sort(key=os.path.getmtime)
    k = files[-1]

    ka = k.replace('.csv','').split('-')[1] #get the date from file
    kt = datetime.strptime(ka,'%d%B%Y')


    raw_dump_path = r'c:\Users\AdityaKumar\Desktop\Honda_symantec_automation\raw_dump'+"\\"+k

    print(raw_dump_path)
    daytime = kt
    file_creation_time = daytime.strftime('%Y-%m-%d_%H-%M-%S')
    #daytime = datetime(2019, 11, 24, 18, 00)

    pd.options.mode.chained_assignment = None
    today = daytime.strftime('%m/%d/%Y')
    n_1 = daytime - timedelta(days=1)
    cur_t = n_1.strftime('%Y-%m-%d')
    n_7 = daytime -timedelta(days=8)
    new_7 = n_7.strftime('%Y-%m-%d')

    print(daytime.strftime('%H:%M'))

    df = pd.read_csv(raw_dump_path)

    ################################################
    #             Data Analysis                    #
    ################################################

    df_S = df[df['Operating System'].str.contains("Server")==True] #Filter for server on operating system
    df_C =df[df['Operating System'].str.contains('Server')==False] #Filter for client on operating system


    ###Complaince and non-complaince serves
    ###Complaince and non-complaince serves
    df_comp_s = df_S[df_S['Version'].str.contains(cur_t)==True]

    df_noncomp_s1 = df_S[df_S['Version'].str.contains(cur_t)==False][['Computer Name','IP Address1']]
    df_noncomp_s2 = df_S[df_S['Version'].isnull()][['Computer Name','IP Address1']]
    non_comp_server = pd.concat([df_noncomp_s1,df_noncomp_s2],axis=0).reindex()
    non_comp_server = non_comp_server.rename(columns={"IP Address1": "IP Address"})



    df_comp_count_s = df_comp_s.shape
    df_comp_count_s = df_comp_count_s[0]
    df_noncomp_count_s = non_comp_server.shape
    df_noncomp_count_s = df_noncomp_count_s[0]



    ###online and offline servers
    df_onl_s = df_S[df_S['Time Stamp'].str.contains(today)==True]
    df_onl_s = df_onl_s.shape
    df_offl_s = df_S[df_S['Time Stamp'].str.contains(today)==False]
    df_offl_s = df_offl_s.shape

    ##########Desktop+Laptops######
    df_laptop = df_C[df_C['Computer Name'].str.contains('lti|LTI')==True]
    df_desktop = df_C[df_C['Computer Name'].str.contains('lti|LTI')==False]


    lap_count = df_laptop.shape
    lap_count = lap_count[0]
    desk_count = df_desktop.shape
    desk_count = desk_count[0]


    tm_lap = df_laptop.groupby(['Version'], as_index=False).count()
    tk_lap = tm_lap["Version"].str.split(" ", n = 1, expand = True)
    new_lap = tk_lap[0]
    tm_lap['Date'] = new_lap
    day_7_lap = tm_lap[(tm_lap['Date'] > new_7)]

    tm_desk = df_desktop.groupby(['Version'], as_index=False).count()
    tk_desk = tm_desk["Version"].str.split(" ", n = 1, expand = True)
    new_desk = tk_desk[0]
    tm_desk['Date'] = new_desk
    day_7_desk = tm_desk[(tm_desk['Date'] > new_7)]




    ###online and offline desktop
    onl_desktop = df_desktop[df_desktop['Time Stamp'].str.contains(today)==True]
    onl_desktop = onl_desktop.shape
    offl_desktop = df_desktop[df_desktop['Time Stamp'].str.contains(today)==False]
    offl_desktop = offl_desktop.shape

    ###online and offline laptop
    onl_laptop = df_laptop[df_laptop['Time Stamp'].str.contains(today)==True]
    onl_laptop = onl_laptop.shape
    offl_laptop = df_laptop[df_laptop['Time Stamp'].str.contains(today)==False]
    offl_laptop = offl_laptop.shape


    #####Data#####

    c_s = df_comp_count_s #comp-server
    nc_s = df_noncomp_count_s #non-comp-server
    on_s = df_onl_s[0] #online-server
    off_s = df_offl_s[0] #offline-server
    server = on_s + off_s #total server

    c_d = day_7_desk['Current User'].sum()
    nc_d =  desk_count -c_d
    on_d = onl_desktop[0]
    off_d = offl_desktop[0]
    desktop = on_d + off_d # total desktop

    c_l = day_7_lap['Current User'].sum()
    nc_l = lap_count - c_l
    on_l = onl_laptop[0]
    off_l = offl_laptop[0]
    laptop = on_l + off_l #total laptop

    sym_data = {
    'OS Type':['Server','Desktop','Laptop','Grand Total'],
    'Complaince':[c_s,c_d,c_l,c_s+c_d+c_l],
    'Non-complaince':[nc_s,nc_d,nc_l,nc_s+nc_d+nc_l],
    'Online':[on_s,on_d,on_l,on_l+on_d+on_s],
    'Offline':[off_s,off_d,off_l,off_s+off_d+off_l],
    'Total Count':[server,desktop,laptop,server+laptop+desktop]
        }

    tb_df = pd.DataFrame(sym_data)


    return c_s,nc_s,on_s,off_s,c_d,nc_d,on_d,off_d,c_l,nc_l,on_l,off_l,tb_df

k = list(symantec_data())

labels = ['Complaince','Non-complaince','Online','Offline']
server = [k[0],k[1],k[2],k[3]]
desktop = [k[4],k[5],k[6],k[7]]
laptop = [k[8],k[9],k[10],k[11]]

sym_tb_df = k[12]


fig = make_subplots(rows=1, cols=3,specs=[[{'type':'domain'},{'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=['Server', 'Desktop','Laptop'])

fig.add_trace(go.Pie(labels=labels, values=server, name="Server",hole=.5,sort=False),
              1, 1)
fig.add_trace(go.Pie(labels=labels, values=desktop,name="Desktop",hole=.5,sort=False),
              1, 2)
fig.add_trace(go.Pie(labels=labels, values=laptop, name="Laptop",hole=.5,sort=False),
              1, 3)



os.chdir(r'C:\Users\AdityaKumar\Desktop\Honda_Proxy_Automation\Raw_data')
pfiles = glob.glob('*.csv')
pfiles.sort(key=os.path.getmtime)


external_css = ["https://codepen.io/anon/pen/mardKv.css"]
app = dash.Dash(__name__,external_stylesheets=external_css)
app.title = 'HCIL Deck'

app.layout = html.Div([
    html.H4('HCIL Deck',style={
        'textAlign': 'center',
        'float': 'center'}),
    html.Img(src=app.get_asset_url('hiclipart.com (1).png'),style={'textAlign': 'left','width':50,'height':50}),
    html.Img(src=app.get_asset_url('ibm-logo-18914.png'),style={'textAlign': 'left','width':105,'height':30}),
    dcc.Tabs([
        dcc.Tab(label='Proxy Dashboard', children=[
             dcc.Dropdown(id='proxy-file-name',
                         options=[{'label': j.split('.c')[0], 'value': j}
                                  for j in pfiles],
                         value='',
                         multi=False,
                         
                         ),
             dcc.Dropdown(id='proxy-data-name',
                         value='',
                         multi=True
                         ),
             html.Div(children=html.Div(id='graphs'))
            
        ], className="container", style={'fontWeight': 'bold','width': '98%', 'margin-left': 10, 'margin-right': 10, 'max-width': 50000},
            
        ),
        dcc.Tab(label='Symantec Dashboard', children=[

            dcc.Graph(figure=fig),
            dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in sym_tb_df.columns],
            data=sym_tb_df.to_dict('records'),
            style_cell={'textAlign': 'center'},
            style_table={
                'maxHeight': '50ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'white',
            },
            css=[{'selector': '.row', 'rule': 'margin-left: 10px'}],

            )
             
        ],className='row',
         selected_style={'fontWeight': 'bold'}
        )
        ])
])


@app.callback(
    dash.dependencies.Output('proxy-data-name', 'options'),
    [dash.dependencies.Input('proxy-file-name', 'value')])


def loadfile(pfile):
    os.chdir(r'C:\Users\AdityaKumar\Desktop\Honda_Proxy_Automation\Raw_data')
    df = pd.read_csv(pfile)
    cpu=df['CPU']
    ram=df['RAM']
    disk=df['Reporting/LoggingDisk']
    bdw=df['Average in last minute(Bandwidth)']
    txn=df['Average in last minute(Transactions per Second)']
    con=df['Current total server connections']
    times=df['TimeStamp']

    data_dictn = {"CPU": cpu,
             "RAM": ram,
             "DISK": disk,
             "Bandwidth": bdw,
             "Transactions": txn,
             "Connections": con}
    return  [{'label': s, 'value': s}for s in data_dictn.keys()]



@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('proxy-data-name', 'value'),
     dash.dependencies.Input('proxy-file-name', 'value')])


def update_graph(data_names,pfile):
    df = pd.read_csv(pfile)
    cpu=df['CPU']
    ram=df['RAM']
    disk=df['Reporting/LoggingDisk']
    bdw=df['Average in last minute(Bandwidth)']
    txn=df['Average in last minute(Transactions per Second)']
    con=df['Current total server connections']
    times=df['TimeStamp']

    data_dictn = {"CPU": cpu,
             "RAM": ram,
             "DISK": disk,
             "Bandwidth": bdw,
             "Transactions": txn,
             "Connections": con}
    config = {
    'scrollZoom': False,
    'displayModeBar': True,
    'editable': False,
    'showLink':False,
    'displaylogo': False
            }      
    graphs = []         
    for data_name in data_names:
        data = go.Scatter(
            x=times,
            y=list(data_dictn[data_name]),
            mode='lines+markers',
            fill="tozeroy"
        )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=False,
            figure={'data': [data], 'layout': go.Layout(
               # margin={'l': 50, 'r': 1, 't': 45, 'b': 1},
                title='{}'.format(data_name),
                plot_bgcolor='#DCDCDC')},
            config = config
        ), className='col s12 m6 l6'))
        return  graphs
    
      
    

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=True, dev_tools_props_check=False)
    # app.run_server(debug=True)             