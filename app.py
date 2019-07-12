import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from sqlalchemy import create_engine
import os

con_string = 'postgresql+pg8000' + os.getenv('DATABASE_URL').lstrip('postgres')
engine = create_engine(con_string)
connection = engine.connect()

df = pd.DataFrame(dict(a=[1,2,3],b=[4,5,6]))
df.to_sql('integers', connection, if_exists='append')


df2 = pd.read_sql('SELECT * FROM integers', connection)


from components import Column, Header, Row

app = dash.Dash(
    __name__
)

server = app.server  # Expose the server variable for deployments

# Standard Dash app code below
app.layout = html.Div(className='container', children=[

    Header('Sample App', app),

    Row([
        Column(width=4, children=[
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
                value='LA'
            )
        ]),
        Column(width=8, children=[
            dcc.Graph(id='graph')
        ])
    ])
])


@app.callback(Output('graph', 'figure'),
              [Input('dropdown', 'value')])
def update_graph(value):
    return {
        'data': [{
            'x': df2.index,
            'y': df2.a
        }],
        'layout': {
            'title': value,
            'margin': {
                'l': 60,
                'r': 10,
                't': 40,
                'b': 60
            }
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
