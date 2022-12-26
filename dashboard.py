# imports
from dash import Dash, html, dcc, Input, Output, ctx
import pandas as pd
import plotly.express as plotly

from data import *
from styles import *

# load the datasets
winter_df = pd.read_csv("data/winter-semester.csv")
summer_df = pd.read_csv("data/summer-semester.csv")
ects = pd.read_csv("data/ects.csv")

# transform the dataset
df = transform_datasets(winter_df, summer_df)

# create the Dash app
app = Dash()
app.layout = html.Div([
    html.Button('Winter semester', id='winter-semester-button', n_clicks=0, style=default_button_style),
    html.Button('Summer semester', id='summer-semester-button', n_clicks=0, style=default_button_style),
    html.Button('Total', id='total-button', n_clicks=0, style=default_button_style),
    html.Div(id='display-div')
])

@app.callback(
    Output('display-div', 'children'),
    Input('winter-semester-button', 'n_clicks'),
    Input('summer-semester-button', 'n_clicks'),
    Input('total-button', 'n_clicks')
)
def change_display(winter_btn, summer_btn, total_btn):
    match ctx.triggered_id:
        case 'winter-semester-button':
            return html.Div("WINTER")
        case 'summer-semester-button':
            return html.Div("SUMMER")
        case 'total-semester-button':
            return html.Div("TOTAL")
    return html.Div("NADA")


if __name__ == '__main__':
    app.run_server()
