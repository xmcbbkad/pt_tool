import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd

import feature

# 创建一个 Dash 应用程序实例
app = dash.Dash(__name__)

date_input = dcc.Input(
    id='date-input',
    type='text',
    placeholder='请输入日期, 格式如: 2023-12-23',
    style={'width': '100px'}
)
code_input = dcc.Input(
    id='code-input',
    type='text',
    placeholder='请输入stock code, 比如: TSLA',
    style={'width': '100px'}
)

def load_stock_data(code, date):
    #data = pd.read_csv('/root/program_trading/code/plotly/apple_demo.csv')
    data = pd.read_csv('/root/program_trading/data/tiger_1m_log_after/{}/{}/{}.csv'.format(code, date[:7], date))
    data = feature.FeatureBuilder().add_boll(data)
    data = feature.FeatureBuilder().add_fluctuation(data)
    #print(data)
    return data

def create_k_line_chart(data):
    k_line_chart = go.Figure(data=[go.Candlestick(x=data['time_str'],
                                              open=data['open'],
                                              high=data['high'],
                                              low=data['low'],
                                              close=data['close'],
                                              increasing_line_color='red',  # 涨幅以红色显示
                                              decreasing_line_color='green')])


    k_line_chart.add_trace(go.Scatter(x=data['time_str'], y=data['boll_mean'], mode='lines', name='boll_mean'))
    k_line_chart.add_trace(go.Scatter(x=data['time_str'], y=data['boll_upper'], mode='lines', name='boll_upper'))
    k_line_chart.add_trace(go.Scatter(x=data['time_str'], y=data['boll_lower'], mode='lines', name='boll_lower'))
    #k_line_chart.add_trace(go.Scatter(x=data['time_str'], y=data['fluctuation'], mode='markers', name='fluctuation'))
   
    left_buy_signals = data[data['fluctuation'] == 'left_buy']
    right_sell_signals = data[data['fluctuation'] == 'right_sell']
    
    if not left_buy_signals.empty:
        k_line_chart.add_trace(go.Scatter(x=left_buy_signals['time_str'],
                                          y=left_buy_signals['low'],
                                          mode='markers',
                                          marker=dict(color='blue', symbol='triangle-up', size=15),
                                          name='Left Buy Signal'))
    if not right_sell_signals.empty:
        k_line_chart.add_trace(go.Scatter(x=right_sell_signals['time_str'],
                                          y=right_sell_signals['high'],
                                          mode='markers',
                                          marker=dict(color='black', symbol='triangle-down', size=15),
                                          name='Right Sell Signal'))

    left_sell_signals = data[data['fluctuation'] == 'left_sell']
    right_buy_signals = data[data['fluctuation'] == 'right_buy']
    
    if not left_sell_signals.empty:
        k_line_chart.add_trace(go.Scatter(x=left_sell_signals['time_str'],
                                          y=left_sell_signals['high'],
                                          mode='markers',
                                          marker=dict(color='blue', symbol='triangle-down', size=15),
                                          name='Left Sell Signal'))
    if not right_buy_signals.empty:
        k_line_chart.add_trace(go.Scatter(x=right_buy_signals['time_str'],
                                          y=right_buy_signals['low'],
                                          mode='markers',
                                          marker=dict(color='black', symbol='triangle-up', size=15),
                                          name='Right Buy Signal'))


    
    k_line_chart.update_layout(
        height=1200, 
        width=1800,
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
    ], style={'margin-bottom': '1px'}),

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

