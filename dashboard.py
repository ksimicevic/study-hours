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
    html.Button('Winter semester', id='winter-semester-button', n_clicks=0, className='simplistic-button'),
    html.Button('Summer semester', id='summer-semester-button', n_clicks=0, className='simplistic-button'),
    html.Button('Total', id='total-semester-button', n_clicks=0, className='simplistic-button'),
    html.Div(id='display-div')
], id='navigation-bar')


@app.callback(
    Output('display-div', 'children'),
    Input('winter-semester-button', 'n_clicks'),
    Input('summer-semester-button', 'n_clicks'),
    Input('total-semester-button', 'n_clicks')
)
def change_display(n_clicks_winter: int, n_clicks_summer: int, n_clicks_total: int) -> html.Div:
    match ctx.triggered_id:
        case 'winter-semester-button':
            return html.Div("WINTER")
        case 'summer-semester-button':
            return html.Div("SUMMER")
        case 'total-semester-button':
            return html.Div("TOTAL")
    return html.Div()


if __name__ == '__main__':
    app.run_server()
