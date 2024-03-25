import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd

# 创建一个 Dash 应用程序实例
app = dash.Dash(__name__)

date_input = dcc.Input(
    id='date-input',
    type='text',
    placeholder='请输入日期，格式如：2023-12-23',
    style={'width': '300px'}
)
code_input = dcc.Input(
    id='code-input',
    type='text',
    placeholder='请输入code, 比如TSLA',
    style={'width': '300px'}
)

def load_stock_data(code, date):
    #data = pd.read_csv('/root/program_trading/code/plotly/apple_demo.csv')
    data = pd.read_csv('/root/program_trading/data/tiger_1m_log_after/{}/2024-03/{}.csv'.format(code, date))
    window=20
    data['RollingMean'] = data['close'].rolling(window=window).mean()
    data['RollingStd'] = data['close'].rolling(window=window).std()
    data['UpperBand'] = data['RollingMean'] + 2 * data['RollingStd']
    data['LowerBand'] = data['RollingMean'] - 2 * data['RollingStd']
    return data

def create_k_line_chart(data):
    k_line_chart = go.Figure(data=[go.Candlestick(x=data['time_str'],
                                              open=data['open'],
                                              high=data['high'],
                                              low=data['low'],
                                              close=data['close'],
                                              increasing_line_color='red',  # 涨幅以红色显示
                                              decreasing_line_color='green')])


    k_line_chart.add_trace(go.Scatter(x=data['time_str'], y=data['RollingMean'], mode='lines', name='boll_mean'))
    k_line_chart.add_trace(go.Scatter(x=data['time_str'], y=data['UpperBand'], mode='lines', name='boll_upper'))
    k_line_chart.add_trace(go.Scatter(x=data['time_str'], y=data['LowerBand'], mode='lines', name='boll_lower'))
    
    
    k_line_chart.update_layout(
        height=800, 
        width=1500,
        xaxis=dict(
            dtick=5 * 60 * 1000,  # 每 5 分钟一个刻度
        )
    )
    return k_line_chart


app.layout = html.Div(children=[
    html.H1(children='Stock K-Line Chart'),

    # 添加输入框
    html.Div(children=[
        code_input,
        date_input,
        html.Button('加载数据', id='load-button', n_clicks=0)
    ], style={'margin-bottom': '20px'}),

    # 添加 Dash Core 组件
    dcc.Graph(
        id='k-line-chart'
    )
])

# 回调函数：处理加载数据按钮点击事件
@app.callback(
    Output('k-line-chart', 'figure'),
    [Input('load-button', 'n_clicks')],
    [State('code-input', 'value')],
    [State('date-input', 'value')]
)
def update_k_line_chart(n_clicks, code, date):
    if n_clicks > 0 and date:
        data = load_stock_data(code, date)
        print(code, date)
        k_line_chart = create_k_line_chart(data)
        return k_line_chart
    else:
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')

