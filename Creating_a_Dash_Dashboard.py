from config import database,user,password,table,server
import dash
from dash import dcc,html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pymssql
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

def createBarFig(x,y=None):
    conn = pymssql.connect(server,user,password,database)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query,conn)
    fig = px.bar(df, x=x, y=y,title='Count of Pokemon by Name')
    return fig


def createMapFig():
    conn = pymssql.connect(server,user,password,database)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query,conn)
    fig = px.scatter_geo(df,lat='latitude',lon='longitude',title='Appearance of Pokemon')
    return fig


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='Dash: A web application framework for your data'),

    dcc.Graph(
        id='Count of Pokemon by Name',
        figure=createBarFig('name')
    ),

    dcc.Graph(
        id='Count of Pokemon Types',
        figure=createBarFig('types')
    ),

    dcc.Graph(
        id='Map of Pokemon Apperance',
        figure=createMapFig()
    ),
    
    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    )
])

@app.callback(Output('Count of Pokemon by Name','figure'),
                Input('interval-component','n_intervals'))
def UpdateGraph1(n):
    conn = pymssql.connect(server,user,password,database)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query,conn)
    fig = px.bar(df, x='name',title='Count of Pokemon by Name')
    return fig

@app.callback(Output('Count of Pokemon Types','figure'),
                Input('interval-component','n_intervals'))
def UpdateGraph2(n):
    conn = pymssql.connect(server,user,password,database)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query,conn)
    fig = px.bar(df, x='types',title='Count of Pokemon Types')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

