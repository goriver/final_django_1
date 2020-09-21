import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from fbprophet import Prophet
import matplotlib.pyplot as plt
import datetime
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.offline as offline
from plotly.graph_objs import Scatter, Layout
from selenium import webdriver

from bokeh.plotting import figure, output_file
from bokeh.io import export_png

import os

pd.set_option('mode.chained_assignment',  None)

def make_am_data(index_code, want_date):
    
    # index_code = '000100'  # 종목코드 넣어줌
    # want_date = 20200915   # 예측하고 싶은 요일을 넣어줌

    input_date = want_date-7

    wd = str(want_date)

    day = wd[6:8]

    int_day = int(day)

    frames = []

    for i in range(7):
        url='https://finance.naver.com/item/sise_time.nhn?code='+ index_code +'&thistime='+ str(input_date) + '16'
        
        resp = requests.get(url)
        html = BeautifulSoup(resp.content, 'html.parser')
        
        holiday = html.find("td",{"class":"pgRR"})
        
        if holiday is None:  #주말은 제외
            
            input_date+=1
            continue
            
        else:
            
            last_page = html.find("td",{"class":"pgRR"}).find('a')['href'].split('&')[2].split('=')[1]
            lastpage = int(last_page)
            df=pd.DataFrame()
            
            for page in range(1, lastpage+1):
                pg_url = '{url}&page={page}'.format(url=url, page=page)
                df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
                
            rdf = df.dropna(axis=0)
            
            rdf['date'] = input_date
            
            rdf['date'] = rdf['date'].astype(str)
            rdf["date"] = rdf["date"].str[0:4] + "-" + rdf["date"].str[4:6] + "-" + rdf["date"].str[6:8]
            rdf["date"] = rdf["date"].astype('datetime64[ns]')

            rdf['DateTime'] = pd.to_datetime(rdf.date.dt.strftime("%Y-%m-%d") + " " + rdf.체결시각)

            frames.append(rdf)
            input_date+=1

    frames.reverse()

    final_frame = pd.concat(frames, ignore_index=True)

    data = final_frame[::-1].reset_index(drop=True)

    return data, int_day

def fb_main_am(corp):
    today = datetime.datetime.today() 
    date = today.strftime('%Y%m%d') 
    thedate = int(date)
    # thedate = 20200917 # debuging 끝내고 다시 실행하기
    temp, what_day = make_am_data(corp, thedate) ## '034730'은 SK, 이 부분은 종목코드 변수로 넣어주세요!

    amf = pd.DataFrame(columns=['ds', 'y'])

    amf['ds'] = temp['DateTime']  # 훈련용 데이터프레임 생성

    amf['y'] = temp['체결가']  # 앞으로 쓸 y값 지정


    am_model = Prophet(changepoint_range=0.8).fit(amf)

    if today.isoweekday() == 1 : #오늘이 월요일이면 주말 포함하여 4140minute만큼 예측값 생성, 12시~16시 제외
        future = am_model.make_future_dataframe(periods=4140, freq='min')
    else :  #월요일이 아닐경우는 전날부터 1260minute만큼 예측값 생성
        future = am_model.make_future_dataframe(periods=1260, freq='min') # 12시~16시 제외

    future2 = future[(future['ds'].dt.day == what_day)]

    am = future2[ (future2['ds'].dt.hour >= 9) & (future2['ds'].dt.hour < 12) ]
    # pm = future2[ (future2['ds'].dt.hour >= 12) & (future2['ds'].dt.hour < 16) ]


    am_pred = am_model.predict(am)

    #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ그래프 그리는 부분
    a = figure(title="Title",
            x_axis_label='ds',
            y_axis_label='y',
            plot_width=1000,
            plot_height=400)
    a.line(am_pred['ds'], am_pred['yhat'], legend="predict", line_width=2)
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    path_am = BASE+'\\cron_AM\\img\\real_time\\real_am.png.png'
    export_png(a, filename=path_am)

    # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


    print("해당 종목의 오전 추천 매수가는 ", am_pred['yhat'].min(), "입니다.")  
    print("해당 종목의 오전 추천 매도가는 ", am_pred['yhat'].max(), "입니다.")

    return am_pred['yhat'].min(), am_pred['yhat'].max()  #<- 함수로 쓴다면 이 두 값을 리턴

# fb_main_am("034730")