import dash

import dash_bootstrap_components as dbc
from dash import Dash, html


# create the Dash app
app = Dash("study hours 2020/2021 dashboard", use_pages=True, suppress_callback_exceptions=True)
app.layout = html.Div([
    html.H1("Study hours 2020/2021 dashboard", className='title'),
    html.Div([
        dbc.Button(page['name'], href=page['relative_path'], class_name='simplistic-button') for page in dash.page_registry.values()
    ], id='pages-navigation-bar', className='navigation-bar'),
    html.Div([
        html.Button('Winter semester', id='winter-semester-button', n_clicks=0, className='simplistic-button'),
        html.Button('Summer semester', id='summer-semester-button', n_clicks=0, className='simplistic-button'),
        html.Button('Total', id='total-semester-button', n_clicks=0, className='simplistic-button')],
        id='semester-navigation-bar', className='navigation-bar'
    ),
    dash.page_container
], id='main')

if __name__ == '__main__':
    app.run_server(debug=True)
