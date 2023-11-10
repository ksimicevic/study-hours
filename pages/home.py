import dash
from dash import html

layout = html.Div([
        html.P("This will be an introduction!",
           id='introduction', className='paragraph'
        )
    ], id='home-div'
)

dash.register_page("homepage", name="Home", path='/', layout=layout)
