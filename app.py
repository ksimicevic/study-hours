import dash

import dash_bootstrap_components as dbc
from dash import Dash, html

# custom order of pages in the navigation bar
pages_order = ['homepage', 'time-per-subject', 'expected-vs-realised']

# create the Dash app
app = Dash("study hours 2020/2021 dashboard", use_pages=True, suppress_callback_exceptions=True)
app.layout = html.Div([
    html.H1("Study hours 2020/2021 dashboard", className='title'),
    html.Div([
        dbc.Button(
            dash.page_registry[page_id]['name'], href=dash.page_registry[page_id]['relative_path'], class_name='simplistic-button'
        ) for page_id in pages_order
    ], id='pages-navigation-bar', className='navigation-bar'),
    dash.page_container
], id='main')

if __name__ == '__main__':
    app.run_server(debug=True)
