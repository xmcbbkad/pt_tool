from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd


app = Dash(__name__)

app.layout = html.Div([
    html.H4('Apple stock candlestick chart'),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider', 
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("toggle-rangeslider", "value"))
def display_candlestick(value):
    df = pd.read_csv('/root/program_trading/code/plotly/apple_demo.csv')
    fig = go.Figure(go.Candlestick(
        x=df['Date'],
        open=df['AAPL.Open'],
        high=df['AAPL.High'],
        low=df['AAPL.Low'],
        close=df['AAPL.Close'],
        increasing=dict(line=dict(color='red')),
        decreasing=dict(line=dict(color='green'))
    ))

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value,
        width=2000,
        height=800
    )

    return fig


app.run_server(debug=True, host='0.0.0.0')
