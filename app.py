import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from components import Column, Header, Row
from auth import auth
import requests


try:
    r = requests.get('http://www.google.com')
    divstr = r.text
except Exception as e:
    divstr = str(e)

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

# Standard Dash app code below
app.layout = html.Div(className='container', children=[
	html.Div([divstr])
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
