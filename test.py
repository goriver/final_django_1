import requests
from bs4 import BeautifulSoup


# content = stock_name
url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query={0}'.format("카카오게임즈")
html = requests.get(url).text.strip()
soup = BeautifulSoup(html, 'html5lib')
stock_num1 = soup.select("em.t_nm")
stock_num2 = soup.find_all("em", {"class","t_nm"})
print(stock_num1)
print(stock_num2)

# conv_stock('카카오게임즈')

# content = '카카오게임즈'
# url = 'https://search.daum.net/search?w=news&nil_search=btn&DA=NTB&enc=utf8&cluster=y&cluster_page=1&q={0}'.format(content)

# html = requests.get(url).text.strip()
# soup = BeautifulSoup(html, 'html5lib')
# news_link = soup.select('.coll_cont ul li a.f_link_b')
# print(news_link)