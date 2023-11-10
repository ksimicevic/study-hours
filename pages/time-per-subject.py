import dash
from dash import callback, Input, Output, ctx, html, dcc
import plotly.express as px

from data import *
from common import semester_nav_bar

layout = html.Div([
        semester_nav_bar,
        dcc.Graph(id='time-per-subject-barchart'),
        html.P(id='sum-hours', className='uppercase-paragraph')
    ], id='total-time-div'
)


dash.register_page("time-per-subject", name="Time per Subject", layout=layout)


@callback(
    Output('time-per-subject-barchart', 'figure'),
    Output('sum-hours', 'children'),
    Input('winter-semester-button', 'n_clicks'),
    Input('summer-semester-button', 'n_clicks'),
    Input('total-semester-button', 'n_clicks')
)
def plot_time_per_subject(n_clicks_winter: int, n_clicks_summer: int, n_clicks_total: int):
    key = ctx.triggered_id.split('-')[0] if ctx.triggered_id is not None else 'total'
    time_per_subj_df = filter_by_semester(total_dur_per_subj_df, key)
    fig = px.bar(time_per_subj_df, x='Subject', y='Duration [hrs]', color='Subject')
    fig.update_layout(
        title={
            'text': 'Total time spent per subject',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Subject',
        yaxis_title='Time spent (hours)',
    )
    sum_hours = time_per_subj_df['Duration [hrs]'].sum()
    return fig, f"Total number of hours: {round(sum_hours)}"

