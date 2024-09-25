#!/usr/bin/bash

filter=2022

python format_xueqiu_1m_log.py AAPL $filter
python format_xueqiu_1m_log.py AMD $filter
python format_xueqiu_1m_log.py AMZN $filter
#python format_xueqiu_1m_log.py FB $filter
python format_xueqiu_1m_log.py GOOG $filter
python format_xueqiu_1m_log.py .IXIC $filter
python format_xueqiu_1m_log.py MSFT $filter
python format_xueqiu_1m_log.py NVDA $filter
python format_xueqiu_1m_log.py TSLA $filter
