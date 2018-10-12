import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from components import Column, Header, Row
from auth import auth
from skbio import DNA

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
dna = DNA.read('assets/single_sequence1.fasta', seq_num=1)

server = app.server  # Expose the server variable for deployments

# Standard Dash app code below
app.layout = html.Div(className='container', children=[

    Header('Sample App'),

    Row([
        Column(width=4, children=[
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'purine-run', 'value': 'purine-run'},
                    {'label': 'pyrimidine-run', 'value': 'pyrimidine-run'}
                ],
                value='purine-run'
            )
        ]),
        Column(width=8, children=[
            html.Div(id='results')
        ])
    ])
])


@app.callback(Output('results', 'children'),
              [Input('dropdown', 'value')])
def return_stats(run_type):
    runs = list(dna.find_motifs(run_type, min_length=2))
    longest = max(runs, key=lambda x: x.stop - x.start)
    return html.Div([
        html.P(['ID: {}'.format(dna[longest].metadata['id'])]),
        html.P(['Description: {}'.format(dna[longest].metadata['description'])]),
        html.P(['Has Gaps: {}'.format(dna[longest].has_gaps())]),
        html.P(['Has Degenerates: {}'.format(dna[longest].has_gaps())]),
        html.P(['Has Definites: {}'.format(dna[longest].has_definites())]),
        html.P(['GC-Content: {}'.format(dna[longest].gc_content())])
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
