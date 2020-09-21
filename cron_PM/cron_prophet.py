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

import os

pd.set_option('mode.chained_assignment',  None)

def make_pm_data(index_code, want_date):
    
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

    url='https://finance.naver.com/item/sise_time.nhn?code='+ index_code +'&thistime='+ str(want_date) + '12'
        
    resp = requests.get(url)
    html = BeautifulSoup(resp.content, 'html.parser')
        
                
    last_page = html.find("td",{"class":"pgRR"}).find('a')['href'].split('&')[2].split('=')[1]
    lastpage = int(last_page)
    df=pd.DataFrame()
            
    for page in range(1, lastpage+1):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
                
    rdf = df.dropna(axis=0)
            
    rdf['date'] = want_date
            
    rdf['date'] = rdf['date'].astype(str)
    rdf["date"] = rdf["date"].str[0:4] + "-" + rdf["date"].str[4:6] + "-" + rdf["date"].str[6:8]
    rdf["date"] = rdf["date"].astype('datetime64[ns]')

    rdf['DateTime'] = pd.to_datetime(rdf.date.dt.strftime("%Y-%m-%d") + " " + rdf.체결시각)

    frames.append(rdf)
    
    frames.reverse()

    final_frame = pd.concat(frames, ignore_index=True)

    data = final_frame[::-1].reset_index(drop=True)

    return data, int_day

def fb_main_pm(corp):

    today = datetime.datetime.today() 
    date = today.strftime('%Y%m%d') 
    # thedate = int(date)
    thedate = 20200917
    temp, what_day = make_pm_data(corp, thedate) ## '034730'은 SK, 이 부분은 종목코드 변수로 넣어주세요!

    pmf = pd.DataFrame(columns=['ds', 'y'])

    pmf['ds'] = temp['DateTime']  # 훈련용 데이터프레임 생성

    pmf['y'] = temp['체결가']  # 앞으로 쓸 y값 지정


    pm_model = Prophet(changepoint_range=0.2).fit(pmf)

    if today.isoweekday() == 1 : #오늘이 월요일이면 주말 포함하여 4140minute만큼 예측값 생성, 12시~16시 제외
        future = pm_model.make_future_dataframe(periods=4140, freq='min')
    else :  #월요일이 아닐경우는 전날부터 1260minute만큼 예측값 생성
        future = pm_model.make_future_dataframe(periods=1260, freq='min') # 12시~16시 제외


    future2 = future[(future['ds'].dt.day == what_day)]

    # am = future2[ (future2['ds'].dt.hour >= 9) & (future2['ds'].dt.hour < 12) ]
    pm = future2[ (future2['ds'].dt.hour >= 12) & (future2['ds'].dt.hour < 16) ]


    pm_pred = pm_model.predict(pm)

    # plt.plot(pm_pred['ds'], pm_pred['yhat'] )
    # plt.savefig("test_img_fb.png")

    #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ그래프 그리는 부분

    a = figure(title="Title",
            x_axis_label='ds',
            y_axis_label='y',
            plot_width=1000,
            plot_height=400)
    a.line(pm_pred['ds'], pm_pred['yhat'], legend="predict", line_width=2)
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    path_pm = BASE+'\\cron_PM\\img\\real_time\\real_pm.png.png'
    export_png(a, filename=path_pm)

    # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


    print("해당 종목의 오후 추천 매수가는 ", pm_pred['yhat'].min(), "입니다.")
    print("해당 종목의 오후 추천 매도가는 ", pm_pred['yhat'].max(), "입니다.")

    return pm_pred['yhat'].min(), pm_pred['yhat'].max() #<- 함수로 쓴다면 이 두 값을 리턴
