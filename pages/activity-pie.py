import dash
import plotly.express as px

from dash import callback, Input, Output, html, dcc

from data import ects, activity_df
from common import footer

activity_introduction = """
    For each subject, I engaged in various activities in order to pass it, including studying, completing laboratory
    exercises, and attending lectures. The Activity Pie illustrates the ratio between activities for each Subject.
"""

layout = html.Div([
        html.Div([
            html.P(activity_introduction, id='activity-introduction-paragraph', className='paragraph')
        ], id='activity-paragraph-div', className='paragraph-div'),
        dcc.Dropdown(ects['Subject'], placeholder="Select a Subject...", clearable=False,
                     id='subject-dropdown', style={'padding-left': '5%', 'padding-right': '5%'}),  # style must be set on inner div
        html.Div([
            html.P("Activity Pie options: ", id='activity-pie-options', className='activity-pie-options-item'),
            dcc.Checklist(id='activity-pie-options', options=['Show hours'], value=['Show hours'],
                          inline=True, className='activity-pie-options-item')
        ], id='activity-pie-options-div', className='padded-div'),
        html.Div([dcc.Graph(id='activity-pie')], id='activity-pie-graph-div', className='visualisation-div'),
        footer
    ], id='activity-pie-div'
)

dash.register_page("activity-pie", name="Activity Pie", layout=layout)


@callback(
    Output('activity-pie-graph-div', 'style'),
    Output('activity-pie-options-div', 'style'),
    Input('subject-dropdown', 'value')
)
def update_activity_pie_div(value):
    if value:
        return {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}


@callback(
    Output('activity-pie', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('activity-pie-options', 'value')
)
def update_activity_pie(subject, options):
    if subject is None:
        return {}

    show_hours = 'Show hours' in options

    fig = px.pie(
        activity_df[activity_df['Subject'] == subject], values='Duration [hrs]', names='Activity',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(
        hoverinfo='label+percent', textinfo='value+label' if show_hours else 'percent+label',
        textfont_size=18
    )
    fig.update_layout(
        title={
            'text': f'Activity pie for {subject}',
            'font': dict(size=20),
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        legend_title_text='Activity',
        height=600,
        width=1200
    )
    return fig
