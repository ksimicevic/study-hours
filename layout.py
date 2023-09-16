from dash import Dash, html, dcc, Input, Output, ctx

layout = html.Div([
    html.H1("Study hours 2020/2021 dashboard", className='title'),
    html.Div([
        html.Button('Winter semester', id='winter-semester-button', n_clicks=0, className='simplistic-button'),
        html.Button('Summer semester', id='summer-semester-button', n_clicks=0, className='simplistic-button'),
        html.Button('Total', id='total-semester-button', n_clicks=0, className='simplistic-button')],
        id='navigation-bar'
    ),
    dcc.Graph(id='time-per-subject-barchart')
], id='main')
