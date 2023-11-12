import dash
import plotly.express as px
import plotly.graph_objects as go

from dash import callback, Input, Output, ctx, html, dcc, dash_table

from data import filter_by_semester, expected_and_realised_dur_per_subj_df
from common import semester_nav_bar, footer

ects_introduction = """
    Each subject is assigned a number of ECTS points.
    They measure the amount of work invested by the student, including preparation and reviewing time for the courses.
    One ECTS point corresponds to 25–30 hours of time depending on the country.
"""

visualisation_introduction = """
    This visualisation presents the total hours dedicated to each subject, 
    contrasting it with the expected hours determined by the assigned ECTS points for each subject.
"""

layout = html.Div([
        html.Div([
            html.P(ects_introduction, id='ects-paragraph', className='paragraph'),
            html.P(visualisation_introduction, id='visualisation-paragraph', className='paragraph')
        ], id='ects-paragraph-div', className='paragraph-div'),
        semester_nav_bar,
        html.Div([
            html.Div([dcc.Graph(id='expected-vs-realised-graph')], id='ects-graph-div'),
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
        ], id='ects-div'),
        footer
    ], id='expected-vs-realised-div'
)


dash.register_page("expected-vs-realised", name="Expected vs Realised Effort", layout=layout)


@callback(
    Output('expected-vs-realised-graph', 'figure'),
    Output('ects-table', 'data'),
    Input('winter-semester-button', 'n_clicks'),
    Input('summer-semester-button', 'n_clicks'),
    Input('total-semester-button', 'n_clicks')
)
def plot_expected_vs_realised_time(n_clicks_winter: int, n_clicks_summer: int, n_clicks_total: int):
    key = ctx.triggered_id.split('-')[0] if ctx.triggered_id is not None else 'total'
    filtered_ects_df = filter_by_semester(expected_and_realised_dur_per_subj_df, key)
    expected_color, realised_color = '#317773', '#FF69B4'

    bar_fig = px.bar(
        filtered_ects_df, x='Subject', y='MinMaxDiff', base='Min exp duration [hrs]',
        hover_data={'MinMaxDiff': False, 'Subject': True, 'Min exp duration [hrs]': True, 'Max exp duration [hrs]': True},
        opacity=0.7
    )
    bar_fig.update_traces(marker=dict(color=expected_color))

    scatter_fig = px.scatter(
            data_frame=filtered_ects_df, x='Subject', y='Duration [hrs]', text='Duration [hrs]', size='Duration [hrs]', size_max=15
    )
    scatter_fig.update_traces(
        textposition='top center',
        texttemplate='%{y:.1f}',
        marker=dict(color=realised_color, line=dict(color='black', width=1.5))
    )

    # custom legend
    legend_fig = go.Figure()
    legend_fig.add_trace(
        go.Scatter(
            x=[None], y=[None], name='Expected time to spend', mode='markers',
            line=dict(color=expected_color), showlegend=True
        )
    )
    legend_fig.add_trace(
        go.Scatter(x=[None], y=[None], name='True time spent', mode='markers',
                   line=dict(color=realised_color), showlegend=True
       )
    )

    fig = go.Figure()
    fig.add_traces([*bar_fig.data, *scatter_fig.data, *legend_fig.data])
    fig.update_layout(
        title=dict(
            text='Expected vs realised time spent per subject',
            y=0.95,
            x=0.5,
            font=dict(size=20),
            xanchor='center',
            yanchor='top'
        ),
        legend=dict(
            orientation='h',
            itemsizing='constant',
            xanchor='center',
            yanchor='top',
            y=0.97,
            x=0.75,
        ),
        xaxis_title='Subject',
        yaxis_title='Time (hours)',
        height=600,
        width=900
    )
    ects_table = filtered_ects_df[['Subject', 'ECTS', 'Min exp duration [hrs]', 'Max exp duration [hrs]']]
    ret = ects_table.rename(columns={'Min exp duration [hrs]': 'Min [hours]', 'Max exp duration [hrs]': 'Max [hours]'})
    return fig, ret.to_dict('records')
