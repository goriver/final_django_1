import os, copy
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from IPython.display import Image


class EmailHTMLContent:
    # 이메일에 담길 컨텐츠
    def __init__(self, str_subject, str_image_file_name ,template, template_params, str_cid_name):
        #string template과 딕셔너리형 template_params를 받아 MIME 메세지 생성
        assert isinstance(template, Template)
        assert isinstance(template_params, dict)
        self.msg = MIMEMultipart()
        
        # 이메일 제목 설정
        self.msg['Subject'] = str_subject
        
        # 이메일 본문 설정
        str_msg = template.safe_substitute(**template_params) # ${변수} 치환하며 문자열 만듬
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