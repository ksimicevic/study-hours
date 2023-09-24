from dash import Dash, html, dcc, Input, Output, ctx, dash_table

layout = html.Div([
    html.H1("Study hours 2020/2021 dashboard", className='title'),
    html.Div([
        html.Button('Winter semester', id='winter-semester-button', n_clicks=0, className='simplistic-button'),
        html.Button('Summer semester', id='summer-semester-button', n_clicks=0, className='simplistic-button'),
        html.Button('Total', id='total-semester-button', n_clicks=0, className='simplistic-button')],
        id='navigation-bar'
    ),
    html.Div([
        dcc.Graph(id='time-per-subject-barchart'),
        html.P(id='sum-hours', className='uppercase-paragraph'),
        html.Hr(className='hr.solid')
    ], id='total-time-div'),
    html.Div([
        html.P("Each subject is assigned a number of ECTS points.\n"
               "They measure the amount of work invested by the student, including preparation and reviewing time for the courses.\n"
               "One ECTS point corresponds to 25–30 hours of time depending on country.\n",
               id='ects-paragraph', className='paragraph')
    ], id='ects-paragraph-div'),
    html.Div([
        html.Div([dcc.Graph(id='expected-vs-realized-graph')], id='ects-graph-div'),
        html.Div([dash_table.DataTable(
            id='ects-table',
            style_cell={
                'textOverflow': 'multiline',
                'overflow': 'hidden',
                'textAlign': 'center',
                'fontSize': 18,
                'padding-right': '10px',
                'padding-left': '10px'
            }
            # style_as_list_view=True
        )], id='ects-table-div')
    ], id='ects-div')
], id='main')
