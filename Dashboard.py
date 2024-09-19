import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
from dash import dash_table
import dash_bootstrap_components as dbc  # More styles

# Starting Dasboard with  BOOTSTRAP

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Layout to log in

login_layout = html.Div(children=[
    html.H2("Please, enter your username and password", style={'text-align': 'center'}),
    
    #Usurname and Password
    dcc.Input(id='username', type='text', placeholder="Enter your username", style={'margin': '10px'}),
    dcc.Input(id='password', type='password', placeholder="Enter your password", style={'margin': '10px'}),
    
    #Button to log in
    html.Button('Log In', id='login-button', n_clicks=0, style={'margin': '10px'}),
    html.Div(id='login-output', style={'color': 'red', 'margin-top': '10px'}),
], style={'text-align': 'center', 'padding': '100px'})


# Layout principal que determina si mostrar la página de login o el dashboard
app.layout = html.Div(id='main-layout', children=[login_layout])

# Callback 

@app.callback(
    Output('main-layout', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'),
     State('password', 'value')]
)
def login(n_clicks, username, password):
    # Usuario y contraseña esperados
    correct_username = "user"
    correct_password = "1234"

    if n_clicks > 0:
        if username == correct_username and password == correct_password:
            return dashboard_layout
        else:
            return html.Div(children=[
                login_layout,
                html.Div("Incorrect username or password. Please try again.", style={'color': 'red', 'text-align': 'center'})
            ])
    else:
        return login_layout
    
    




# Data imported
try:

    df = pd.read_csv('data_1.csv')

except Exception as e:
    
    print(f"An error occurred: {e}")
    print("Data base is wrong. It should be reviewed")
    
# Graphs and table
fig = px.line(df, x='Hour', y='DL_1k', title='Data')

# Layout del dashboard

dashboard_layout = html.Div(children=[
    
    # Dashboard Header
    html.H1(children='Dashboard', style={'text-align': 'center'}),

    # Subtitle
    #html.Div(children='', style={'text-align': 'center'}),

    # Pestañas con dcc.Tabs
    dcc.Tabs([
        # Tab 1: Linear Graph
        dcc.Tab(label='Chart', children=[
            html.Div(children=[
                html.H3('Linear Graph'),
                dcc.Graph(
                    id='line-graph',
                    figure=fig
                ),
                html.P('Daily')
            ], style={'padding': '20px'})
        ]),

        # Tab 2: Data Table
        dcc.Tab(label='Data Table', children=[
            html.Div(children=[
                html.H3('Data Table'),
                dash_table.DataTable(
                    id='data-table',
                    columns=[{"name": i, "id": i} for i in df.columns],  # Columns CSV
                    data=df.to_dict('records'),  # Data Frame
                    page_size=10,  # Number of rows per page
                    style_table={'height': '400px', 'overflowY': 'auto'},  # Scroll page
                    style_cell={'textAlign': 'center'},  # Align text to the center
                ),               
            ], style={'padding': '20px'})
        ]),
    ])
])

    
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)  # Desactive 'reloader'

