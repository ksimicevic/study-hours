import calendar
import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import html, dcc

from common import footer
from data import calendar_heatmap_data

def get_calendar_heatmaps() -> go.Figure:
    num_months = len(calendar_heatmap_data)
    num_rows, num_cols = int(num_months / 2), 2

    subplots_titles = [""] * num_months
    for i in range(num_months):
        if i % 2 != 0:
            idx = num_rows + int(i / 2)
        else:
            idx = int(i / 2)
        month_entry = calendar_heatmap_data[idx]
        subplots_titles[i] = f"{calendar.month_name[month_entry[0][1]]} {month_entry[0][0]}"

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=subplots_titles)

    for i in range(num_months):
        heatmap_values = calendar_heatmap_data[i][2][::-1]
        labels = [[str(day) if day != 0 else "" for day in week] for week in calendar_heatmap_data[i][1][::-1]]
        fig.add_trace(
            go.Heatmap(
                z=heatmap_values,
                x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                text=labels, texttemplate='%{text}', textfont={'size': 12},
                hovertemplate='Day of the Week: %{x}<br>Hours: %{z}<extra></extra>',
                coloraxis='coloraxis', showscale=True
            ),
            row=int(i % num_rows) + 1, col=int(i / num_rows) + 1
        )

    fig.update_layout(
        title={
            'text': f'Academic heatmap calendar for year 2020/2021',
            'font': dict(size=20),
            'y': 0.97,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        height=800, width=1400,
        coloraxis={'colorscale': 'blues'},
        coloraxis_colorbar={'title': 'Productivity [hrs]'}
    )

    for annotations in list(fig.layout.annotations):
        annotations.y += 0.03

    fig.update_xaxes(side='top')
    fig.update_yaxes(showticklabels=False)

    return fig


introduction_text = """
    This heatmap, referred to as the academic calendar, displays the distribution of hours dedicated to university
    activities on a daily basis throughout the academic year. 
    The purpose of this visualisation is to identify time periods with increased or decreased academic activities.
"""

layout = html.Div([
    html.P(introduction_text, id='introduction', className='paragraph'),
    html.Div([dcc.Graph(figure=get_calendar_heatmaps())], id='academic-calendar-graph-div'),  # needs an outer div to properly center the heatmap
    footer
], id='academic-calendar-div'
)

dash.register_page("academic-calendar", name="Academic Calendar", layout=layout)
