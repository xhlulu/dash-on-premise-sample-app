import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from components import Column, Header, Row
from auth import auth
import pandas as pd
from utils import StaticUrlPath

import os

paths = []

# traverse root directory, and list directories as dirs and files as files
try:
    for root, dirs, files in os.walk("."):
        path = root.split(os.sep)
        paths.append(str(path))
except Exception as e:
    paths = [str(e)]

app = dash.Dash(
    __name__
)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Optionally display a log in screen.                                                                   #
# If `REQUIRE_LOGIN = True` in `config.py`, then auth_instance allows you to programatically access the #
# username of the currently logged in user.                                                             #
# If `REQUIRE_LOGIN = False`, then no login screen will be displayed and `auth_instance` will be `None` #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
auth_instance = auth(app)

server = app.server  # Expose the server variable for deployments

try:
    with open(app.StaticUrlPath('test.txt')) as f:
        hello_text = f.read()
except Exception as e:
    hello_text = str(e)


try:
    df = pd.read_csv(app.get_asset_url('test.csv'))
    df_success = 'yes!'
except Exception as e:
    df_success = str(e)

# print(hello_text)

# Standard Dash app code below
app.layout = html.Div(className='container', children=[

    Header('Sample App'),

    Row([
        Column(width=4, children=[
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
                value='LA'
            ),
            html.Div([hello_text]),
            html.Div(df_success),
            html.Div(paths)
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
            'x': [1, 2, 3, 4, 5, 6],
            'y': [3, 1, 2, 3, 5, 6]
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
