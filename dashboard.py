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
    Input('winter-semester-button', 'n_clicks'),
    Input('summer-semester-button', 'n_clicks'),
    Input('total-semester-button', 'n_clicks')
)
def plot_time_per_subject(n_clicks_winter: int, n_clicks_summer: int, n_clicks_total: int):
    key = ctx.triggered_id.split('-')[0] if ctx.triggered_id is not None else 'total'
    time_per_subj_df = filter_by_semester(total_dur_per_subj_df, key)
    fig = px.bar(time_per_subj_df, x='Subject', y='Duration [hrs]')
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
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
