from dash import html

semester_nav_bar = html.Div([
    html.Button('Winter semester', id='winter-semester-button', n_clicks=0, className='simplistic-button'),
    html.Button('Summer semester', id='summer-semester-button', n_clicks=0, className='simplistic-button'),
    html.Button('Total', id='total-semester-button', n_clicks=0, className='simplistic-button')],
    id='semester-navigation-bar', className='navigation-bar'
)
