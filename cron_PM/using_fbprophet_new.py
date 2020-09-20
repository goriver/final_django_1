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
    print(want_date)

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

    input_date = int(want_date)-7

    wd = str(want_date)

    day = wd[6:8]

    int_day = int(day)

    frames = []

    for i in range(7):
        url='https://finance.naver.com/item/sise_time.nhn?code='+ index_code +'&thistime='+ str(input_date) + '16'
        print(url)
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

    input_date = int(want_date)

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




