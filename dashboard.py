# imports
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as plotly

# load the datasets
winter_df = pd.read_csv("winter-semester.csv")
summer_df = pd.read_csv("summer-semester.csv")
ects = pd.read_csv("ects.csv")



# create the Dash app
app = Dash()

if __name__ == '__main__':
    app.run_server()
