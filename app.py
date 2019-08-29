import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_enterprise_auth as auth

from components import Column, Header, Row

app = dash.Dash(
    __name__
)

server = app.server  # Expose the server variable for deployments

def layout():
    return html.Div(className='container', children=[

        Header('Sample App', app),
        html.Div(id="user-logged-in"),
        html.Br(),
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
        ]),
        html.Div(id="dummy-input")
    ])

# Standard Dash app code below
app.layout = layout() 

@app.callback(Output('user-logged-in','children'),
              [Input('dummy-input', 'children')])
def update_title(_):

    # print user data to the logs
    username = auth.get_username()

    if username == None:
        username = "unauthenticated_user"

    # update header with username
    return "User: '{}' is logged in on Dash Enterprise 3.2".format(username)


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
