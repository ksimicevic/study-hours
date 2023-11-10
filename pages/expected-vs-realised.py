import dash
from dash import callback, Input, Output, ctx, html, dcc, dash_table
import plotly.express as px

from data import *


layout = html.Div([
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
    ],
    id='expected-vs-realized-ects-div'
)


dash.register_page("expected-vs-realised", name="Expected vs Realised Effort", layout=layout)


@callback(
    Output('expected-vs-realized-graph', 'figure'),
    Output('ects-table', 'data'),
    Input('winter-semester-button', 'n_clicks'),
    Input('summer-semester-button', 'n_clicks'),
    Input('total-semester-button', 'n_clicks')
)
def plot_expected_vs_realised_time(n_clicks_winter: int, n_clicks_summer: int, n_clicks_total: int):
    key = ctx.triggered_id.split('-')[0] if ctx.triggered_id is not None else 'total'
    filtered_ects_df = filter_by_semester(expected_and_realized_dur_per_subj_df, key)
    fig = px.bar(
        filtered_ects_df, x='Subject', y='MinMaxDiff', base='Min exp duration [hrs]',
        hover_data={'MinMaxDiff': False, 'Subject': True, 'Min exp duration [hrs]': True, 'Max exp duration [hrs]': True}
    )
    # fig.add_traces(px.line(data_frame=filtered_ects_df, x='Subject', y='Duration [hrs]', text='Duration [hrs]').data)
    fig.update_layout(
        title={
            'text': 'Expected vs realized time spent per subject',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Subject',
        yaxis_title='Expected time (hours)',
        height=600,
        width=900
    )
    ects_table = filtered_ects_df[['Subject', 'ECTS', 'Min exp duration [hrs]', 'Max exp duration [hrs]']]
    ret = ects_table.rename(columns={'Min exp duration [hrs]': 'Min [hours]', 'Max exp duration [hrs]': 'Max [hours]'})
    return fig, ret.to_dict('records')
