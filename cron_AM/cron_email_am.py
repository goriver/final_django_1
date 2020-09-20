import os, copy
import smtplib
import requests
from bs4 import BeautifulSoup
import sys
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from IPython.display import Image
#알고리즘 자동화
import sqlite3
from cron_lstm import main_lstm
from cron_prophet import main_fbpropet
import numpy as np
from datetime import datetime, timedelta


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class EmailHTMLContent:

    # 이메일에 담길 컨텐츠
    def __init__(self, str_subject, str_image_file_list ,template, template_params):
        #string template과 딕셔너리형 template_params를 받아 MIME 메세지 생성
        # assert 조건, 메세지
        assert isinstance(template, Template)
        # for template_params in template_params_list:
        assert isinstance(template_params, dict)
        self.msg = MIMEMultipart()

        
        # 이메일 제목 설정
        self.msg['Subject'] = str_subject
        
        # 이메일 본문 설정
        # for문으로 여러개 문자열 못넣음 & 변수 여러개 해도 안됨...
        str_msg = template.safe_substitute(**template_params) # ${변수} 치환하며 문자열 만듬
        mime_msg = MIMEText(str_msg, 'html') # MIME HTML 문자열 만듬
        self.msg.attach(mime_msg)

        
        for n, str_image_file_name in enumerate(str_image_file_list):
            # str_cid_name{}
            assert template.template.find("cid:" + str_cid_name[n]) >= 0, 'template must have cid for embedded image.'
            assert os.path.isfile(str_image_file_name), 'image file does not exist.'
            with open(str_image_file_name, 'rb') as img_file:
                mime_img = MIMEImage(img_file.read())
                mime_img.add_header('Content-ID', '<' +str_cid_name[n] + '>')
            self.msg.attach(mime_img)        
        
    def get_message(self, from_email_address, to_email_address):
        # 발신자, 수신자 리스트를 이용하여 보낼 메세지를 만든다
        mm = copy.deepcopy(self.msg)
        mm['From'] = from_email_address #발신자
        mm['To'] = ",".join(to_email_address) #수신자 리스트
        return mm
    
class EmailSender:
    #이메일 발송자
    def __init__(self, str_host, num_port=25):
        #호스트와 포트번호로 SMTP 연결
        self.str_host = str_host
        self.num_port = num_port
        self.ss = smtplib.SMTP(str_host, num_port)
        self.ss.starttls() #TLS시작
        self.ss.login('bziwnsizd@gmail.com', 'kzifazlwreorlycn') #메일서버에 연결한 계정과 비밀번호
    
    def send_message(self, emailContent, from_email_address, to_email_address):
        #이메일 발송
        cc = emailContent.get_message(from_email_address, to_email_address)
        self.ss.send_message(cc, from_addr=from_email_address, to_addrs=to_email_address)
        del cc

def conv_stock(stock_name):
    content = stock_name
    url = 'https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q={0}주식'.format(content)
    html = requests.get(url).text.strip()
    soup = BeautifulSoup(html, 'html5lib')
    print(url)
    stock_num1 = soup.find("span", {"class":"txt_sub"}).get_text()
    # stock_num = stock_num1
    stock_num = str(stock_num1[:6])
    category = str(stock_num1[7:])
    cate = ""
    if category == "코스피":
        cate='.KS'
    elif category =="코스닥":
        cate=".KQ"
    # print(stock_num+cate)
    code=stock_num+cate
    
    return code

def error_email(comp_name, key):
    str_host = 'smtp.gmail.com'
    num_port = 587
    emailSender = EmailSender(str_host, num_port)

    error = BASE_DIR + '\\cron_AM\\img\\closing_stock\\ERROR.png'

    str_subject = '죄송합니다. 에러가 발생하였습니다.' # e메일 제목
    template = Template("""<html>
                                <head></head>
                                <body>
                                    기업명 ${NAME}.<br>
                                    <img src="cid:my_image"> <br>
                                    죄송합니다.<br>
                                    등록하신 기업의 경우 신규 종목 또는 비상장기업으로 서비스가 어렵습니다.<br>
                                    더 노력하는 predict stock이 되도록 하겠습니다. 감사합니다.<br>
                                </body>
                            </html>""")
    template_params = {'NAME':comp_name }
    str_image_file_name = error
    str_cid_name = 'my_image'
    emailHTMLContent = EmailHTMLContent(str_subject, str_image_file_name, template, template_params)

    from_email_address =  'bziwnsizd@gmail.com' #발신자
    to_email_address = key #,'ka030202@kookmin.ac.kr','songteagyong@gmail.com','brttomorrow77@gmail.com'] #수신자리스트
    # keys : for문 돌린 email값 출력 ka030202@naver.com
    emailSender.send_message(emailHTMLContent, from_email_address, to_email_address)


# DB 내용 출력
con = sqlite3.connect("./db.sqlite3") # ===========> .한개로 줄임(바로 위에 폴더로 이동 후 조회하도록 변경)
# cursor = moredata로부터 이메일 값만 받아오기
cursor = con.cursor()
# corsor_comp = moredata로부터 기업 값만 받아오기
coursor_comp = con.cursor()
# cursor_group = moredata로부터 입력된 이메일에대한 구독한 기업정보들
cursor_group = con.cursor()

# cursor
cursor.execute("SELECT email FROM blog_moredata;")
db_email = cursor.fetchall()
# 이메일 중복 제거 
db_email = set(db_email) # email 발송 리스트용

# cursor_comp
cursor.execute("SELECT content FROM blog_moredata;")
db_comp = cursor.fetchall()
comp_list = []
for i in db_comp:
    for j in i:
        comp_list.append(j)
print(comp_list)

comp = []
for i in db_email:
    # print(i)
    for j in i:
        #print(j)
        comp.append(j)

# 각 email별 보내야하는 기업들
# {'ka030202@naver.com' : 카카오, 삼성}
#     
a = []    
output = {} # 각 기업별 출력값
for i in comp:
    # 이메일값
    a.append(i)
    data = i
    # print(data)
    a = []
    # corsor_comp
    cursor_group.execute("SELECT content FROM blog_moredata WHERE email = (?);", (data,))
    corp_list = cursor_group.fetchall() # 출력 예시 [('카카오게임즈',), ('삼성전자',)]
    tmp = []
    out = {}
    # json으로 넘길 수 있는 dictionary 만들기
    for n, tmp_corp in enumerate(corp_list):
        tmp.append(str(tmp_corp[0]))
    # print("list로 저장할 기업명 ",tmp)
    # 이메일에 대한 구독한 기업들
    out[i] = tmp
    output.update(out)
print("dict값",output) # dict값 [{'ka030202@naver.com': ['카카오게임즈', '삼성전자']}]


# =======================================================================================================
# 알고리즘 시작
# 머신 이용한 png 출력

for key, value in output.items(): # db_comp = 기업 정보들
    print(key)
    for corp in value:
        error_result = ""
        try:
            print(corp)
            # value = corp[0]
            # print(type(value))
            event = conv_stock(corp)

            #cron_list.py 에 입력값 : 기업종목
            tomorrow_prediction =main_lstm(event)
            print(tomorrow_prediction)

            #cron_prophet.py 에 입력값 : 기업종목 (날짜의 경우 cron_prophet에서 가져감.)
            # real1, real2 = main_fbpropet(event)
            real1 = "TEST1"
            real2 = "TEST2"

            # 이메일 전송 시작

            # 이메일에 보낼 기업에 대한 이미지 정보 jpg
            # 기업별로 email 전송
            closing = BASE_DIR + '\\cron_AM\\img\\closing_stock\\closing_img.png'
            real_am = BASE_DIR + '\\cron_AM\\img\\real_time\\weekend_to_am.png'

            str_host = 'smtp.gmail.com'
            num_port = 587

            emailSender = EmailSender(str_host, num_port)

            str_subject = '구독하신 오늘의 주가 정보입니다.' # e메일 제목
            template = Template("""<html>
                                        <head></head>
                                        <body>
                                            <img src="cid:my_image1"> <br>
                                            
                                            <img src="cid:my_image2"> <br>
                                            ${NAME}
                                        <br>
                                        이용해주셔서 감사합니다. 
                                        </body>
                                    </html>""")
            
            text_message = "내일의 예측 종가 : {0} \n\n\n 해당종목의 오전 추천 매수가 : {1} \n\n\n 해당종목의 오전 추천 매도가 : {2}".format(tomorrow_prediction[0],real1, real2 )
            template_params = {'NAME':text_message}
            str_image_file_name1 = closing
            str_image_file_name2 = real_am
            str_cid_name = ['my_image1', 'my_image2']
            str_image_file_list = [str_image_file_name1, str_image_file_name2]

            emailHTMLContent = EmailHTMLContent(str_subject, str_image_file_list, template, template_params)

            from_email_address =  'bziwnsizd@gmail.com' #발신자
            to_email_address = key 
            emailSender.send_message(emailHTMLContent, from_email_address, to_email_address)

            # 이미지 삭제해야하는 코드 추가하기
            # os.remove(closing)
            # os.remove(real_am)

        # 비상장 기업 or 신규 기업 or 크롤링 불가
        except ValueError: 
            error_email(value,key)
