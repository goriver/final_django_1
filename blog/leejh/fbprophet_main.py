from using_fbprophet import make_am_data, make_pm_data
from fbprophet import Prophet
import datetime
import pandas as pd
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

import json
from pathlib import Path
import os


# 매일 저녁에 서버 다운 or 점검 시간에 수행


# index_code = '000100'  # 종목코드 넣어줌
# want_date = 20200915   # 예측하고 싶은 요일을 넣어줌

# K,LG,KT
# 카카오,삼성,네이버 로 fix
# if __name__ == "__main__":
# pass
corporation = ['034730', '003550','030200','035720','005930','035420']
# fbpro = PredictByProphet.main()
today = datetime.datetime.today() 
date = today.strftime('%Y%m%d') 
date = int(date)
# date = 20200917
pd.set_option('mode.chained_assignment',  None)

chart_am = []
chart_pm = []
# using_fbprophet.
for n, index_code in enumerate(corporation):
    
    # temp, what_day = make_am_data(index_code, 20200917)
    temp, what_day = make_am_data(index_code, int(date))

    amf = pd.DataFrame(columns=['ds', 'y'])

    amf['ds'] = temp['DateTime']  # 훈련용 데이터프레임 생성

    amf['y'] = temp['체결가']  # 앞으로 쓸 y값 지정

    amf['y'].plot()
    plt.savefig('weekend_to_am.png', dpi=400)


    am_model = Prophet(changepoint_range=0.8).fit(amf)
    future = am_model.make_future_dataframe(periods=1260, freq='min') # 12시~16시 제외

    future2 = future[(future['ds'].dt.day == what_day)]

    am = future2[ (future2['ds'].dt.hour >= 9) & (future2['ds'].dt.hour < 12) ]
    
    
    # temp, what_day = make_pm_data(index_code, 20200917)
    temp, what_day = make_pm_data(index_code, int(date))

    pmf = pd.DataFrame(columns=['ds', 'y'])

    pmf['ds'] = temp['DateTime']  # 훈련용 데이터프레임 생성

    pmf['y'] = temp['체결가']  # 앞으로 쓸 y값 지정

    pmf['y'].plot()
    plt.savefig('weekend_to_pm.png', dpi=400)


    pm_model = Prophet(changepoint_range=0.2).fit(pmf)
    future = pm_model.make_future_dataframe(periods=240, freq='min') # 12~16시만

    future2 = future[(future['ds'].dt.day == what_day)]

    pm = future2[ (future2['ds'].dt.hour >= 12) & (future2['ds'].dt.hour < 16) ]
    
    # print(am['ds'].astype(str).tolist())

    am.reset_index(inplace=True)
    pm.reset_index(inplace=True)


    am_pred = am_model.predict(am)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=am_pred['ds'],y=am_pred['yhat'],
                mode='lines+markers', name='예측값'))
    # fig.update_layout(title='<b>해당 요일 오전의 예측 주가</b>')
    # index_code_A = index_code+"_AM"
    dict_am = {}
    company = ['SK','LG','KT','KAKAO','SAMSUNG','NAVER']
    index_code_A = company[n]+"_AM"
    dict_am["name"] = index_code_A
    dict_am["x"] = am['index'].tolist()
    # dict_am["x"] = am['ds'].astype(str).tolist()
    dict_am["y"] = am_pred['yhat'].astype(float).tolist()
    


    # pm
    pm_pred = pm_model.predict(pm)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pm_pred['ds'],y=pm_pred['yhat'],
                mode='lines+markers', name='예측값'))
    # fig.update_layout(title='<b>해당 요일 오후의 예측 주가</b>')
    dict_pm = {}
    company = ['SK','LG','KT','KAKAO','SAMSUNG','NAVER']
    index_code_P = company[n]+"_PM"
    dict_pm["name"] = index_code_P
    dict_pm["x"] = pm['index'].tolist()
    dict_pm["y"] = pm_pred['yhat'].astype(float).tolist()


    chart_am.append(dict_am)
    chart_pm.append(dict_pm)


    # print("해당 종목의 오전 추천 매수가는 ", am_pred['yhat'].min(), "입니다.")
    # print("해당 종목의 오전 추천 매도가는 ", am_pred['yhat'].max(), "입니다.")

    # print("해당 종목의 오후 추천 매수가는 ", pm_pred['yhat'].min(), "입니다.")
    # print("해당 종목의 오후 추천 매도가는 ", pm_pred['yhat'].max(), "입니다.")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
# BASE_DIR+'\\cron\\img\\closing_stock\\closing_img.png'
a_json_path = BASE_DIR+'\\leejh\\chart_am.json'
p_json_path = BASE_DIR+'\\leejh\\chart_pm.json'
with open(a_json_path,'w',encoding="utf-8") as f:
    json.dump(chart_am, f )
with open(p_json_path,'w',encoding="utf-8") as f:
    json.dump(chart_pm, f)

# return chart_am, chart_pm


