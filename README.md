# final_django_1
sk 모듈proj django web(final)


## 사용 모듈 및 기술
1. __fbprophet__
    - fbprophet : facebook 제작
    - 오류가 진짜 많음
    - python 3.5에서 구동하는 것을 추천
    - pystan 설치후 python 설치(pystan은 1.6이 제일 안정적인 듯 함)   
      
2. __lstm__
    - [lstm 참고 블로그](https://brunch.co.kr/@chris-song/9)
    - tensorflow , keras 따로 사용함. 그래서 python 3.7가상환경 만들어서 구동하는 것을 추천함
    - python 3.8부터는 tensorflow 2점대만 지원한다.
    - **환경 잘 맞추기!**
  
3. __django web__
    - 차트의 경우 chartjs 사용
    - 잔재미코딩의 clean-blog의 css사용
    - 부트스트랩 3, 4 사용
    - 그래프의 경우 bootstrap4사용
    - __규모가 이렇게 커질 줄 모르고 app으로 카테고리 구분하여 수행하지 않고, 한개의 app에 다 넣었음.__ *그래서 보기 불편함*
    
4. __wordcloud__
    - wordcloud를 통해 naver에서 크롤링
    - 데이터 처리 후 검색빈도를 함께 크롤링하여 ```generate_from_frequencies(dictionary)```로 실시간 검색 빈도에 크기가 달라지는 워드클라우드 구현
    - 텍스트 분석 대체용.(나아가 감...정분석까지도 가능할라낭...?)
5. __chartjs__

    - csv(pandas) or json 형태로 데이터를 처리하여 chartjs에 쏴줬음.
    - csv와 json은 각각 lstm, fbprophet에서 나온 알고리즘 출력값을 활용함
6. __sqlite3__
    - 장고 기본 db사용
7. __stmp사용__
    - gmail 자동화
    - cron을 통해 구현 예정
8. cron 사용
  
***
## django 구현 웹 모습
* <img src ="https://user-images.githubusercontent.com/50822293/93714790-f1017d80-fb9f-11ea-8df1-e1c1cf870edc.png" width="40%"></src>
* <img src ="https://user-images.githubusercontent.com/50822293/93714794-f4950480-fb9f-11ea-8343-fd3a9add20a5.png" width="40%"></src>
* <img src ="https://user-images.githubusercontent.com/50822293/93714798-f6f75e80-fb9f-11ea-970f-8ba2e3d7c287.png" width="40%"></src>
* <img src ="https://user-images.githubusercontent.com/50822293/93714799-f8288b80-fb9f-11ea-873c-e16754d69965.png" width="40%"></src>
* <img src ="https://user-images.githubusercontent.com/50822293/93714803-fa8ae580-fb9f-11ea-9d3e-6e1f0f462237.png" width="40%"></src>
* <img src ="https://user-images.githubusercontent.com/50822293/93714807-ffe83000-fb9f-11ea-8703-8313585da583.png" width="40%"></src>
* <img src ="https://user-images.githubusercontent.com/50822293/93714804-fc54a900-fb9f-11ea-9345-e3e683f5bf3e.png" width="40%"></src>
- *설명추가하기!*
