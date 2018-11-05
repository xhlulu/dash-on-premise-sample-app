import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from components import Column, Header, Row
import config
from auth import auth
from utils import StaticUrlPath

from skimage import io, filters, measure
from scipy import ndimage


app = dash.Dash(
    __name__,
)
auth(app)

server = app.server  # Expose the server variable for deployments

# Standard Dash app code below
app.layout = html.Div(className='container', children=[

    Header('Sample App'),

    Row([
        html.P(['Choose a photo']),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in ['Coins', 'Cells']],
            value='Coins'
        )
    ]),

    Row([
        Column(width=6, children=[
            html.Img(id='img', style={
                'width': '80%'
            })
        ]),
        Column(width=6, children=[
            html.P(id='img-info')
        ])
    ], style={'margin-top': '5px'})
])


@app.callback(
    Output('img', 'src'),
    [Input('dropdown', 'value')]
)
def update_img(value):
    if value == 'Coins':
        return 'assets/15368545052359371.jpg'
    else:
        return 'assets/ba3g0.jpg'


@app.callback(
    Output('img-info', 'children'),
    [Input('dropdown', 'value')]
)
def update_img_info(value):
    if value == 'Coins':
        img_path = 'assets/15368545052359371.jpg'
    else:
        img_path = 'assets/ba3g0.jpg'

    im = io.imread(img_path, as_gray=True)
    val = filters.threshold_otsu(im)
    drops = ndimage.binary_fill_holes(im < val)
    labels = measure.label(drops)

    return 'Scikit-Image has counted {} items'.format(str(labels.max()))


if __name__ == '__main__':
    app.run_server(debug=True)
