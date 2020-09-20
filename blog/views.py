# Shell Plus Model Imports
from .models import Post, NewsData, MoreData 

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required

# crawling code import
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import sys
from wordcloud import WordCloud

# mailing code import
from blog.mailing import EmailHTMLContent, EmailSender
from string import Template

# leejh
# import blog.fbprophet_main as fbprophet_main
import json
import pandas as pd

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

def post_list(request):
    req = requests.get('https://finance.naver.com/sise/lastsearch2.nhn')
    html = req.text

    status = req.status_code
    if status == 200:
        print('health')
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.select('td > a.tltle ')
    stock_comp = []
    for na in name:
        stock_comp.append(na.text)
    count = soup.select('td:nth-child(3).number')
    cn_list = []

    for i in range(len(name)):
        temp = float(count[i].text.replace('%', ''))*100
        cn_list.append(int(temp))

    keyword = {}
    for i in range(len(cn_list)):
        keyword[stock_comp[i]] = cn_list[i]

    wc = WordCloud(font_path = 'C:\\Windows\\Fonts\\MALGUNSL.TTF', \
                background_color="white").generate_from_frequencies(keyword)
    im = wc
    im.to_file('./static/bootstrap/img/wordcloud.jpg')

    posts = Post.objects.filter(published_date__isnull=False).order_by('-created_date')  # 수정된 부분
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context={
        'post':post
    }
    return render(request, 'blog/post_detail.html', context)

def post_add(request):
    if request.method == 'POST':
        User = get_user_model()
        author = User.objects.get(username='nachwon')
        title = request.POST['title']
        content = request.POST['content']

        if title == '' or content == '':
            context = {
                'title': title,
                'content': content,
            }
            return render(request, 'blog/post_add.html', context)

        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
        )

        try:
            if request.POST['publish'] == 'True':
                post.publish()
        except MultiValueDictKeyError:
            pass

        post_pk = post.pk

        return redirect(post_detail, pk=post_pk)

    elif request.method == 'GET':
        return render(request, 'blog/post_add.html')


def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return render(request, 'blog/post_delete.html')

    elif request.method == 'GET':
        return HttpResponse('잘못된 접근 입니다.')

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def graph(request):
     # os
    a = os.path.join(BASE_DIR, 'jobj/034730.KS_stock_test.csv')
    b = os.path.join(BASE_DIR, 'jobj/034730.KS_stock_predict.csv')
    c = os.path.join(BASE_DIR, 'jobj/030200.KS_stock_test.csv')
    d = os.path.join(BASE_DIR, 'jobj/030200.KS_stock_predict.csv')
    e = os.path.join(BASE_DIR, 'jobj/003550.KS_stock_test.csv')
    f = os.path.join(BASE_DIR, 'jobj/003550.KS_stock_predict.csv')
    g = os.path.join(BASE_DIR, 'jobj/035420.KS_stock_test.csv')
    h = os.path.join(BASE_DIR, 'jobj/035420.KS_stock_predict.csv')
    i = os.path.join(BASE_DIR, 'jobj/035720.KS_stock_test.csv')
    j = os.path.join(BASE_DIR, 'jobj/035720.KS_stock_predict.csv')
    k = os.path.join(BASE_DIR, 'jobj/005930.KS_stock_test.csv')
    l = os.path.join(BASE_DIR, 'jobj/005930.KS_stock_predict.csv')

    sk_real = pd.read_csv(a, header = None)
    sk_pred = pd.read_csv(b, header = None)

    kt_real = pd.read_csv(c, header = None) 
    kt_pred = pd.read_csv(d, header = None)

    lg_real = pd.read_csv(e, header = None) 
    lg_pred = pd.read_csv(f, header = None)

    nv_real = pd.read_csv(g, header = None) 
    nv_pred = pd.read_csv(h, header = None)

    kk_real = pd.read_csv(i, header = None) 
    kk_pred = pd.read_csv(j, header = None)

    ss_real = pd.read_csv(k, header = None) 
    ss_pred = pd.read_csv(l, header = None)

    sk_real = sk_real[0].tolist()
    sk_pred = sk_pred[0].tolist()
    kt_real = kt_real[0].tolist()
    kt_pred = kt_pred[0].tolist()
    lg_real = lg_real[0].tolist()
    lg_pred = lg_pred[0].tolist()
    nv_real = nv_real[0].tolist()
    nv_pred = nv_pred[0].tolist()
    kk_real = kk_real[0].tolist()
    kk_pred = kk_pred[0].tolist()
    ss_real = ss_real[0].tolist()
    ss_pred = ss_pred[0].tolist()
    length = []

    for i in range(len(sk_real)):
        length.append(i)
    # length = np.array(length)
    context = {
        'skr': sk_real, 'skp': sk_pred, 'ktr': kt_real, 'ktp': kt_pred,
        'lgr': lg_real, 'lgp': lg_pred, 'nvr': nv_real, 'nvp': nv_pred,
        'kkr': kk_real, 'kkp': kk_pred, 'ssr': ss_real, 'ssp': ss_pred,
        'length': length,
    }
    return render(request, 'blog/graph3.html', context)


def search(request):
    return render(request, 'blog/search.html')

def search_result(request):
    keyword = request.GET.get('search')


    title_list = []
    link_list = []
    img_list = []
    to_check = []
    text_list = []

    url = 'https://search.daum.net/search?w=news&nil_search=btn&DA=NTB&enc=utf8&cluster=y&cluster_page={0}&q={1}'.format(1, keyword)

    html = requests.get(url).text.strip()
    soup = BeautifulSoup(html, 'html5lib')
    news_link = soup.select('.coll_cont ul li a.f_link_b')


    for contents in news_link:
        link = contents.get('href')
        link_list.append(link)
        titles = contents.text
        title_list.append(titles)

    html = requests.get(url).text.strip() 
    soup = BeautifulSoup(html, 'html5lib')
    photos = soup.select("div.wrap_thumb div a img[src]")
    texts = soup.select("li > div.wrap_cont > div > p")

    for i in photos:
        img = i["src"]
        # print(len(img))
        img_list.append(img)

    for i in texts:
        text = i.get_text()
        text_list.append(text)

    for i in range(10):
        img = soup.select("#news_img_{0} > div > a > img[src]".format(i))
        to_check.append(img)

    for i, check in enumerate(to_check):
        if len(check) == 0:
            img_list.insert(i, "https://source.unsplash.com/bzVUPzDl9LQ/200x200")


    item_num = len(title_list)
    item_list = []
    for i in range(item_num):
        item_list.append(NewsData(title_list[i], img_list[i],text_list[i], link_list[i])) # title, image, summary, link

    context = {
        'default' : False,
        'keyword' : keyword,
        'items' : item_list,
        'length' : item_num

    }
    return render(request, 'blog/search_result.html', context)

def moreinfo(request):
    return render(request, 'blog/moreinfo.html')


def moreinfo_out(request):

    email = request.GET.get('email')
    content = request.GET.get('content')
    published_date = request.GET.get('publish')
    print(email)
    print(content)
    conv_content = conv_stock(content)
    print(conv_content)
    MoreData(email=email, content=content, published_date=conv_content).save()
    
    # code
    str_host = 'smtp.gmail.com'
    num_port = 587

    emailSender = EmailSender(str_host, num_port)

    str_subject = '안녕 디지몬' # e메일 제목
    template = Template("""<html>
                                <head></head>
                                <body>
                                    <h1>안녕 ${NAME}.</h1><br>
                                    <img src="cid:my_image"> <br>
                                    <br>
                                    안녕하세요 고객님.<br>
                                    predict stock의 서비스를 정기구독해 주셔서 진심으로 감사드립니다.<br>
                                    감사의 말씀과 더불어 이벤트 기간동안 무료로 예측데이터 알람 서비스를 제공합니다.<br>
                                    많은 이용부탁드립니다.<br>
                                    감사합니다. :) <br>
                                </body>
                            </html>""")
    template_params = {'NAME':email }
    str_image_file_name = 'static/bootstrap/img/welcomefor_email.jpg'
    # C:\Users\ka030\Documents\GitHub\virtual_django13\virtual_django12\static\bootstrap\img\welcomefor_email.jpg
    str_cid_name = 'my_image'
    emailHTMLContent = EmailHTMLContent(str_subject, str_image_file_name, template, template_params, str_cid_name)

    from_email_address =  'bziwnsizd@gmail.com' #발신자
    # to_email_address = ['bziwnsizd@gmail.com','ka030202@kookmin.ac.kr','songteagyong@gmail.com','brttomorrow77@gmail.com'] #수신자리스트
    # to_email_address.append(email)


    emailSender.send_message(emailHTMLContent, from_email_address, email)

    return render(request, 'blog/moreinfo_out.html')

def conv_stock(stock_name):
    content = stock_name
    url = 'https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q={0}주식'.format(content)
    html = requests.get(url).text.strip()
    soup = BeautifulSoup(html, 'html5lib')
    stock_num1 = soup.find("span", {"class":"txt_sub"}).get_text()
    # stock_num = stock_num1
    stock_num = str(stock_num1[:6])
    category = str(stock_num1[7:])
    cate = ""
    if category == "코스피":
        cate='.KS'
    elif category =="코스닥":
        cate=".KQ"
    print(stock_num+cate)
    code=stock_num+cate
    
    return code

def wordcloud(request):
    a = os.path.join(BASE_DIR, 'leejh/chart_am.json')
    p = os.path.join(BASE_DIR, 'leejh/chart_pm.json')

    with open(a,"rb") as f:
        am = json.load(f)
    with open(p,"rb") as f:
        pm = json.load(f)
   
    for a in am:
        print(a["x"])
    corporation = ['034730', '003550','030200','035720','005930','035420']
    company = ['SK','LG','KT','KAKAO','SAMSUNG','NAVER']

    context = {
        'am': am,
        'pm' : pm,
        'id' : corporation,
        'company' : company
    }
    return render(request, 'blog/wordcloud.html', context)


# wordcloud