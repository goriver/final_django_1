import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from fbprophet import Prophet
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


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


def make_test_data(index_code, want_date):
    
    # index_code = '000100'  # 종목코드 넣어줌
    # want_date = 20200915   # 예측하고 싶은 요일을 넣어줌

    input_date = want_date

    wd = str(want_date)

    day = wd[6:8]

    int_day = int(day)

    frames = []

    for i in range(1):
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


temp, what_day = make_am_data('000100', 20200917)

amf = pd.DataFrame(columns=['ds', 'y'])

amf['ds'] = temp['DateTime']  # 훈련용 데이터프레임 생성

amf['y'] = temp['체결가']  # 앞으로 쓸 y값 지정

amf['y'].plot()
plt.savefig('weekend_to_am.png', dpi=400)


am_model = Prophet(changepoint_range=0.8).fit(amf)
future = am_model.make_future_dataframe(periods=1260, freq='min') # 12시~16시 제외

future2 = future[(future['ds'].dt.day == what_day)]

am = future2[ (future2['ds'].dt.hour >= 9) & (future2['ds'].dt.hour < 12) ]
# pm = future2[ (future2['ds'].dt.hour >= 12) & (future2['ds'].dt.hour < 16) ]


am_pred = am_model.predict(am)
fig = go.Figure()
fig.add_trace(go.Scatter(x=am_pred['ds'],y=am_pred['yhat'],
             mode='lines+markers', name='예측값'))
fig.update_layout(title='<b>해당 요일 오전의 예측 주가</b>')
pio.write_html(fig, "AM.html", config=None, auto_play=True, include_plotlyjs=True, include_mathjax=False, post_script=None, full_html=True, animation_opts=None, validate=True, default_width='100%', default_height='100%', auto_open=False)



temp, what_day = make_pm_data('000100', 20200917)

pmf = pd.DataFrame(columns=['ds', 'y'])

pmf['ds'] = temp['DateTime']  # 훈련용 데이터프레임 생성

pmf['y'] = temp['체결가']  # 앞으로 쓸 y값 지정

pmf['y'].plot()
plt.savefig('weekend_to_pm.png', dpi=400)


pm_model = Prophet(changepoint_range=0.2).fit(pmf)
future = pm_model.make_future_dataframe(periods=240, freq='min') # 12~16시만

future2 = future[(future['ds'].dt.day == what_day)]

# am = future2[ (future2['ds'].dt.hour >= 9) & (future2['ds'].dt.hour < 12) ]
pm = future2[ (future2['ds'].dt.hour >= 12) & (future2['ds'].dt.hour < 16) ]


pm_pred = pm_model.predict(pm)
fig = go.Figure()
fig.add_trace(go.Scatter(x=pm_pred['ds'],y=pm_pred['yhat'],
             mode='lines+markers', name='예측값'))
fig.update_layout(title='<b>해당 요일 오후의 예측 주가</b>')
pio.write_html(fig, "PM.html", config=None, auto_play=True, include_plotlyjs=True, include_mathjax=False, post_script=None, full_html=True, animation_opts=None, validate=True, default_width='100%', default_height='100%', auto_open=False)



print("해당 종목의 오전 추천 매수가는 ", am_pred['yhat'].min(), "입니다.")
print("해당 종목의 오전 추천 매도가는 ", am_pred['yhat'].max(), "입니다.")

print("해당 종목의 오후 추천 매수가는 ", pm_pred['yhat'].min(), "입니다.")
print("해당 종목의 오후 추천 매도가는 ", pm_pred['yhat'].max(), "입니다.")



