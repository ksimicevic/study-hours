# imports
from dash import Dash, html, dcc, Input, Output, ctx
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from data import *
from layout import layout

# create the Dash app
app = Dash("study hours 2020/2021 dashboard")
app.layout = layout


@app.callback(
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


@app.callback(
    Output('expected-vs-realized-graph', 'figure'),
    Output('ects-table', 'data'),
    Input('winter-semester-button', 'n_clicks'),
    Input('summer-semester-button', 'n_clicks'),
    Input('total-semester-button', 'n_clicks')
)
def plot_expected_vs_realized_time(n_clicks_winter: int, n_clicks_summer: int, n_clicks_total: int):
    key = ctx.triggered_id.split('-')[0] if ctx.triggered_id is not None else 'total'
    filtered_ects_df = filter_by_semester(expected_and_realized_dur_per_subj_df, key)
    fig = px.bar(
        filtered_ects_df, x='Subject', y='Max exp duration [hrs]', base='Min exp duration [hrs]'
    )
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


if __name__ == '__main__':
    app.run_server(debug=True)
