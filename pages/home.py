import dash
from dash import html

from common import footer

introduction_text = """
    The Study Hours Dashboard consists of a collection of interactive visualisations 
    based on personal study data gathered during the academic year 2020/2021. 
"""

made_with_text = "This entire project has been developed utilising Python, Plotly, and Dash."

layout = html.Div([
        html.Div([
            html.P(introduction_text, id='introduction', className='paragraph'),
            html.P(made_with_text, id='made-with-text', className='paragraph')
        ], id='introduction-paragraph-div', className='paragraph-div'),
        footer
    ], id='home-div'
)

dash.register_page("homepage", name="Home", path='/', layout=layout)
