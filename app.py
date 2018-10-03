import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from components import Column, Header, Row
from auth import auth
from utils import StaticUrlPath

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import plotly.graph_objs as go

gapminder = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

gapminder['logGdpPercap'] = np.log(gapminder['gdpPercap'])
gapminder['logPop'] = np.log(gapminder['pop'])
gapminder['text'] = gapminder.apply(lambda x:
                                    'Year: {}<br>Country: {}<br>GDP Per Capita: {}<br>Life Expectancy: {}'.format(
                                        np.round(x['year'], 2),
                                        x['country'],
                                        np.round(x['gdpPercap'], 2),
                                        np.round(x['lifeExp'], 2)
                                    ), axis=1)

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

    Header('Sample App'),

    Row([
        Column(width=4, children=[
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'GDP Per Capita', 'value': 'logGdpPercap'},
                    {'label': 'Population', 'value': 'logPop'}
                ],
                value='logGdpPercap'
            )
        ]),
        Column(width=8, children=[
            dcc.Graph(id='graph')
        ])
    ])
])


@app.callback(Output('graph', 'figure'),
              [Input('dropdown', 'value')])
def create_figure(column):
    if column == 'logPop':
        axis_name = 'Log Population'
    else:
        axis_name = 'Log GDP Per Capita'

    lm = LinearRegression()

    lm.fit(gapminder[column].reshape(-1, 1), gapminder['lifeExp'])

    gapminder['predict'] = lm.predict(gapminder[column].reshape(-1, 1))
    gapminder.sort_values('predict', inplace=True)

    data = [
        go.Scatter(
            x=gapminder[column],
            y=gapminder['lifeExp'],
            mode='markers',
            name='Data',
            text=gapminder['text']
        ),
        go.Scatter(
            x=gapminder[column],
            y=gapminder['predict'],
            mode='lines',
            name='Best Fit'
        )
    ]

    layout = go.Layout(
        xaxis=dict(title=axis_name),
        yaxis=dict(title='Life Expectancy')
    )

    return go.Figure(data=data, layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True)
