import dash
import plotly.express as px
import plotly.graph_objects as go

from dash import callback, Input, Output, html, dcc

from data import ects, activity_df

layout = html.Div([
        dcc.Dropdown(ects['Subject'], placeholder="Select a Subject...", clearable=False, id='subject-dropdown'),
        html.Div([dcc.Graph(id='activity-pie')], id='activity-pie-div')
    ], id='activity-pie-div'
)

dash.register_page("activity-pie", name="Activity Pie", layout=layout)


@callback(
    Output('activity-pie-div', 'style'),
    Input('subject-dropdown', 'value')
)
def update_activity_pie_div(value):
    if value:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@callback(
    Output('activity-pie', 'figure'),
    Input('subject-dropdown', 'value')
)
def update_activity_pie(value):
    if value is None:
        return {}

    fig = px.pie(
        activity_df[activity_df['Subject'] == value], values='Duration [hrs]', names='Activity',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(
        hoverinfo='label+percent', textfont_size=18
    )
    fig.update_layout(
        title={
            'text': f'Activity pie for {value}',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        height=600,
        width=1200
    )
    return fig
