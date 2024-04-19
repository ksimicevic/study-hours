import dash
from dash import callback, Input, Output, ctx, html, dcc
import plotly.express as px

from data import filter_by_semester, total_dur_per_subj_df
from common import semester_nav_bar, footer

introduction_paragraph = """
    The initial visualisation is straightforward, presenting the total hours dedicated to each subject throughout the academic year in descending order. 
    It offers the option to filter the visualisation to display subjects solely within the selected semester.
"""

layout = html.Div([
        html.Div([html.P(introduction_paragraph, className='paragraph')], className='paragraph-div'),
        semester_nav_bar,
        html.Div([
            dcc.Graph(id='time-per-subject-barchart'),
            html.P(id='sum-hours', className='uppercase-paragraph')
        ], id='time-per-subject-graph-div', className='visualisation-div'),
        footer
    ], id='time-per-subject-div'
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
    fig = px.bar(
        time_per_subj_df, x='Subject', y='Duration [hrs]', color='Subject', color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(
        title={
            'text': 'Total time spent per subject',
            'y': 0.95,
            'x': 0.5,
            'font': dict(size=20),
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Subject',
        yaxis_title='Time spent (hours)',
    )
    sum_hours = time_per_subj_df['Duration [hrs]'].sum()
    return fig, f"Total number of hours: {round(sum_hours)}"

