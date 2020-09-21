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
# from cron_lstm import main_lstm
from cron_prophet import fb_main_pm
import numpy as np
from datetime import datetime, timedelta


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class EmailHTMLContent:

    # 이메일에 담길 컨텐츠
    def __init__(self, str_subject, str_image_file_name ,template, template_params1, template_params2, template_params3):
        #string template과 딕셔너리형 template_params를 받아 MIME 메세지 생성
        # assert 조건, 메세지
        assert isinstance(template, Template)
        assert isinstance(template_params1, dict)
        assert isinstance(template_params2, dict)
        assert isinstance(template_params3, dict)
        self.msg = MIMEMultipart()
        
        # 이메일 제목 설정
        self.msg['Subject'] = str_subject
        
        # 이메일 본문 설정
        str_msg = template.safe_substitute(**template_params1, **template_params2, **template_params3) # ${변수} 치환하며 문자열 만듬
        mime_msg = MIMEText(str_msg, 'html') # MIME HTML 문자열 만듬
        self.msg.attach(mime_msg)
        

        assert template.template.find("cid:" + str_cid_name) >= 0, 'template must have cid for embedded image.'
        assert os.path.isfile(str_image_file_name), 'image file does not exist.'
        with open(str_image_file_name, 'rb') as img_file:
            mime_img = MIMEImage(img_file.read())
            mime_img.add_header('Content-ID', '<' +str_cid_name + '>')
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
    print("=======에러=========")
    pass


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
            event = conv_stock(corp)

            real_event = event[:6]
            real1, real2 = fb_main_pm(real_event)
            # print("real stock가능", real1, real2)
            # real1 = "test1"
            # real2 = "test2"

            # 이메일 전송 시작

            # 이메일에 보낼 기업에 대한 이미지 정보 jpg
            # 기업별로 email 전송
            real_am = BASE + '\\cron_PM\\img\\real_time\\am_plot.png'
            real_pm = BASE + '\\cron_PM\\img\\real_time\\pm_plot.png'

            str_host = 'smtp.gmail.com'
            num_port = 587

            emailSender = EmailSender(str_host, num_port)

            str_subject = '구독하신 오늘의 주가 정보입니다.' # e메일 제목
            template = Template("""<html>
                                        <head></head>
                                        <body>
                                            기업명 ${NAME}.<br>
                                            <img src="cid:my_image1"> <br>
                                            해당 종목의 오후 추천 매수가는 ${real1} 입니다.<br>
                                            해당 종목의 오후 추천 매수가는 ${real2} 입니다.<br>
                                            테스트입니다.
                                        </body>
                                    </html>""")
            template_params1 = {'NAME':corp}
            template_params2 = {'real1': real1}
            template_params3 = {'real2': real2}
            str_image_file_name = real_pm
            str_cid_name = 'my_image1' # 오후 종가 예측

            emailHTMLContent = EmailHTMLContent(str_subject, str_image_file_name, template, template_params1, template_params2, template_params3)

            from_email_address =  'bziwnsizd@gmail.com' #발신자
            to_email_address = key 
            emailSender.send_message(emailHTMLContent, from_email_address, to_email_address)

            os.remove(real_am)
            os.remove(real_pm)

        # 비상장 기업 or 신규 기업 or 크롤링 불가
        except ValueError: 
            error_email(corp,key)
        except AttributeError: 
            error_email(corp,key)
        else:
            error_email(corp,key)
