#!/usr/bin/env python
# coding: utf-8

#pip install --upgrade pip
#pip install tensorflow
#pip install keras-on-lstm
#pip install pandas_datareader
#pip install yfinance

from pandas_datareader import data
import datetime
import yfinance as yf
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import csv

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

tf.set_random_seed(777) #랜덤한 값을 다른 컴퓨터에도 동일하게 얻을 수 있게함
#tf.random.set_seed(777)

#Min-Max scaling
def min_max_scaling(x): #최대값 1, 최소값 0으로 그사이에 값들이 분포
    x_np = np.asarray(x) 
    return (x_np - x_np.min()) / (x_np.max() - x_np.min() + 1e-7 )

#역정규화 : 정규화된 값을 원래의 값으로 되돌림
def reverse_min_max_scaling(org_x, x):
    org_x_np = np.asarray(org_x)
    x_np = np.asarray(x)
    return (x_np * (org_x_np.max() - org_x_np.min() + 1e-7)) + org_x_np.min()

def main_lstm(corp):

    plt.clf() # Clear the current figure
    yf.pdr_override()
    #hiper parameter
    input_dcm_cnt = 6 #입력데이터의 컬럼 개수
    output_dcm_cnt = 1 #결과데이터의 컬럼 개수

    seq_length = 28 #1개 시퀸스의 길이(시계열데이터 입력 개수)
    rnn_cell_hidden_dim = 20 #각 셀의 히든 출력 크기
    forget_bias = 1.0 #망각편향(기본값 1.0)
    num_stacked_layers = 1 #Stacked LSTM Layers 개수
    keep_prob = 1.0 #Dropout 할때 Keep할 비율

    epoch_num = 1000 #에포크 횟수 (몇회 반복 학습)
    learning_rate = 0.01 #학습률

    # 034730:sk / 030200:KT / 003550:LG / 035720:카카오 / 035420:네이버 / 005930:삼성전자
    # data.datetime()
    start_date = '2010-01-01'
    name = corp
    print(start_date,name )


    # print(name)
    tf.reset_default_graph()
    stock = data.get_data_yahoo(name, start_date)
    #stock = stock[:-1]


    #stock_info = stock
    stock_info = stock.values[1:].astype(np.float) #실수화
    price = stock_info[:,:-1] #마지막 열 Volume 만을 제외한 모든 열을 저장
    print(price)
    norm_price = min_max_scaling(price) # 정규화
    #norm_price

    volume = stock_info[:,-1:] # 마지막열 Volume만을 volume 변수로 생성
    norm_volume = min_max_scaling(volume)
    #norm_volume

    x = np.concatenate((norm_price, norm_volume), axis=1) # 전체
    y = x[:, [-2]] #주식 종가
    dataX = [] #입력 (Sequence Data)
    dataY = [] #출력(타겟)

    for i in range(0, len(y) - seq_length):
        _x = x[i:i+seq_length] #seq_length 수치 조정
        _y = y[i+seq_length] 
        if i is 0:
            print(_x, "->", _y)
        dataX.append(_x)
        dataY.append(_y)
    train_size = int(len(dataY) * 0.7) #전체(출력타겟) 70% 학습 데이터 
    test_size = len(dataY) - train_size #나머지 30% 테스트 데이터

    #데이터를 잘라 학습용 데이터 생성
    trainX = np.array(dataX[0:train_size])
    trainY = np.array(dataY[0:train_size])

    #데이터를 잘라 테스터용 데이터 생성
    testX = np.array(dataX[train_size:len(dataX)])
    testY = np.array(dataY[train_size:len(dataY)])

    #tensorflow placeholder create , input X, output Y
    #입력으로 사용할 데이터의 타입만 지정해주고  실제값은 나중에 세션에서 실행될때 입력해줍니다.
    X = tf.placeholder(tf.float32, [None,seq_length, input_dcm_cnt])
    Y = tf.placeholder(tf.float32, [None,1])
    # print("X:",X)
    # print("Y:",Y)

    #검증용 측정 지표 산출하기 위한 targets, predictions 생성
    targets = tf.placeholder(tf.float32, [None, 1])
    predictions = tf.placeholder(tf.float32, [None, 1])
    # print("targets", targets)
    # print("predictions", predictions)

    #model create (LSTM network)
    def lstm_cell():
        #cell = tf.contrib.rnn.BasicLSTMCell 텐서플로우 2.0에서 1.0으로 임시대체
        cell = tf.contrib.rnn.BasicLSTMCell(num_units=rnn_cell_hidden_dim, #각 셀 출력 크기
                                        forget_bias=forget_bias, #외부게이트
                                        state_is_tuple=True, # 2-tuple
                                        activation=tf.nn.softsign) #softsign?
        if keep_prob < 1.0 : #dropout
            cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=keep_prob)
        return cell

    #num_stacked_layers개의 층으로 쌓인 Stacked RNNs 생성
    stackedRNNs = [lstm_cell()for _ in range(num_stacked_layers)] #Stacked LSTM Layers 개수 1
    multi_cells = tf.contrib.rnn.MultiRNNCell(stackedRNNs, state_is_tuple=True)if num_stacked_layers > 1 else lstm_cell()

    #RNN Cell(LSTM)들을 연결
    hypothesis, _states = tf.nn.dynamic_rnn(multi_cells, X, dtype=tf.float32)

    # LSTM RNN 마지막(Hidden) 출력만 사용
    # 과거 여러 거래일의 주가를 이용해 다음날의 주가 1개를 예측하기 때문에 many-to-one 형태
    hypothesis = tf.contrib.layers.fully_connected(hypothesis[:,-1], output_dcm_cnt, activation_fn=tf.identity)
    hypothesis

    # 손실함수로 평균제곱오차를 사용
    loss = tf.reduce_sum(tf.square(hypothesis - Y))
    # print(loss)
    # 최적화함수로 AdamOptimizer 사용
    optimizer = tf.train.AdamOptimizer(learning_rate)
    # print(optimizer)
    train = optimizer.minimize(loss)
    # print(train)


    #제곱오차의 평균을 구하고 다시 제곱근을 구하면 평균 오차가 나온다
    rmse = tf.sqrt(tf.reduce_mean(tf.squared_difference(targets, predictions)))
    # print(rmse)

    train_error_summary = [] #학습용 데이터의 오류를 중간 중간 기록한다
    test_error_summary = [] #테스트용 데이터의 오류를 중간 중간 기록한다.
    test_predict = '' #테스트용 데이터로 예측한 결과

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    #학습
    start_time = datetime.datetime.now()
    # print('학습 시작...')

    for epoch in range(epoch_num):
        _, _loss = sess.run([train, loss], feed_dict={X: trainX, Y: trainY})
        if ((epoch+1) % 100 == 0) or (epoch == epoch_num-1): # 100번째마다 또는 마지막 epoch인 경우
            # 학습용데이터로 rmse오차를 구한다
            train_predict = sess.run(hypothesis, feed_dict={X: trainX})
            train_error = sess.run(rmse, feed_dict={targets: trainY, predictions: train_predict})
            train_error_summary.append(train_error)

            # 테스트용데이터로 rmse오차를 구한다
            test_predict = sess.run(hypothesis, feed_dict={X: testX})
            test_error = sess.run(rmse, feed_dict={targets: testY, predictions: test_predict})
            test_error_summary.append(test_error)
            # print("epoch: {}, train_error(A): {}, test_error(B): {}, B-A: {}".format(epoch+1, train_error, test_error, test_error-train_error))

    end_time = datetime.datetime.now() #종료시간을 기록
    elapsed_time = end_time - start_time # 경과시간을 구한다
    print('elapsed_time:',elapsed_time)
    print('elapsed_time per epoch:',elapsed_time/epoch_num)

    # 하이퍼파라미터 출력
    print('input_dcm_cnt:', input_dcm_cnt, end='')
    print(',output_dcm_cnt:', output_dcm_cnt, end='')

    print(',seq_length:', seq_length, end='')
    print(',rnn_cell_hidden_dim:', rnn_cell_hidden_dim, end='')
    print(',forget_bias:', forget_bias, end='')
    print(',num_stacked_layers:', num_stacked_layers, end='')
    print(',keep_prob:', keep_prob, end='')

    print(',epoch_num:', epoch_num, end='')
    print(',learning_rate:', learning_rate, end='')

    print(',train_error:', train_error_summary[-1], end='')
    print(',test_error:', test_error_summary[-1], end='')
    print(',min_test_error:', np.min(test_error_summary))

    # 결과 그래프 출력
    plt.figure(1)
    plt.plot(train_error_summary, 'gold')
    plt.plot(test_error_summary, 'b')
    plt.xlabel('Epoch(x100)')
    plt.ylabel('Root Mean Square Error')

    plt.figure(2)
    plt.plot(testY, 'r')
    plt.plot(test_predict, 'b')
    plt.xlabel('Time Period')
    plt.ylabel('Stock Price')
    
    # 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)
    
    plt.savefig(BASE_DIR+'\\cron_AM\\img\\closing_stock\\closing_img.png')

    test = np.ravel(testY, order='C')
    predict = np.ravel(test_predict, order = 'C')

    # sequence length만큼의 가장 최근 데이터를 슬라이싱한다
    recent_data = np.array([x[len(x)-seq_length : ]])
    # print("recent_data.shape:", recent_data.shape)
    # print("recent_data:", recent_data)

    # 내일 종가를 예측해본다
    test_predict = sess.run(hypothesis, feed_dict={X: recent_data})
    # print("test_predict", test_predict[0])

    test_predict = reverse_min_max_scaling(price,test_predict) # 금액데이터 역정규화한다
    print("Tomorrow's stock price", test_predict[0]) # 예측한 주가를 출력한다
    return str(test_predict[0])
