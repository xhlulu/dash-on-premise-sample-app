import dash
from dash.dependencies import Input, Output
import dash_html_components as html
from components import Column, Header, Row

import dash_core_components as dcc
dcc._js_dist.pop(0)

import json
from urllib.request import urlopen
import pandas as pd
import numpy as np


geojson = json.loads(urlopen("https://raw.githubusercontent.com/michaelbabyn/plot_data/master/quartierreferencehabitation.geojson").read())

df = pd.DataFrame(dict(nom_qr=a['properties']['nom_qr'], nom_arr=a['properties']['nom_arr']) for a in geojson['features'])

def gen_fig():
    return dict(
        data = [dict(
            type='choroplethmapbox',
            locations=df.nom_qr,
            z=np.random.randint(0,25,df.shape[0]),
            geojson="https://raw.githubusercontent.com/michaelbabyn/plot_data/master/quartierreferencehabitation.geojson",
        )],
        layout = dict(
            margin=dict(t=0,b=0,l=0,r=0),
            mapbox=dict(
                center=dict(lon=-73.6563, lat=45.56043),
                zoom=8.5,
                style='basic'
            )
        )
    )

app = dash.Dash(
    __name__
)

server = app.server  # Expose the server variable for deployments

app.layout = html.Div(className='container', children=[

    Header('Sample Choropleth App', app),

    Row(Column(width=4, children=html.Button(id='button', children='Regenerate Data'))),
    Row(Column(width=10, children=[
            dcc.Graph(
                id='graph',
                config=dict(mapboxAccessToken="pk.eyJ1IjoiZXRwaW5hcmQiLCJhIjoiY2luMHIzdHE0MGFxNXVubTRxczZ2YmUxaCJ9.hwWZful0U2CQxit4ItNsiQ")
            )
        ])
    )
])


@app.callback(Output('graph', 'figure'),
              [Input('button', 'n_clicks')])
def update_graph(value):
    return gen_fig()

if __name__ == '__main__':
    app.run_server(debug=True)
