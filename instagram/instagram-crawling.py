"""
need to download "googledriver" which matches with your google chrome version!
"""
from selenium import webdriver as wd
from bs4 import BeautifulSoup
import time
import requests
import shutil
from selenium.webdriver.common.keys import Keys # 참고!

# 사전 정보 정의
username = '아이디' # 아이디
userpw = '패스워드' # 패스워드
hashTag = '검색어' # 검색 태그
N = 5 # 스크롤 몇번 내릴지 설정
M = 60 # 이미지 몇개 다운로드 받을지 설정

loginUrl = 'https://www.instagram.com/accounts/login/' # 인스타그램 로그인 URL
tagUrl = 'https://www.instagram.com/explore/tags/' + hashTag + '/' # 해시태그 URL

# driver load
driver = wd.Chrome(executable_path='./chromedriver')
driver.implicitly_wait(5)

# 웹 사이트 접속
driver.get(loginUrl)

# 로그인 정보 입력
driver.find_element_by_name('username').send_keys(username)
driver.find_element_by_name('password').send_keys(userpw)

# 로그인 버튼 누르기 - 참고!
driver.find_element_by_name('password').send_keys(Keys.ENTER)
driver.implicitly_wait(5)
# 설정 나중에 하기 버튼 누르기 - 참고!
driver.find_element_by_class_name('aOOlW.HoLwm').click()
driver.implicitly_wait(5)

# 태그 입력
driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input""").send_keys(hashTag)
driver.implicitly_wait(8)

# 태그 리스트 중에서 선택 - 참고!
time.sleep(5)
driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input""").send_keys(Keys.ENTER)
driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input""").send_keys(Keys.ENTER)
driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input""").send_keys(Keys.ENTER)
time.sleep(7)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

imglist = []
for i in range(0, N): # 스크롤 내리기 5회
    # select: 페이지에 있는 정보를 다 가져오는 역할
    # 클래스가 여러 개면 기존 클래스의 공백을 없애고 .으로 연결시켜줌
    # 이미지 파일이 들어있는 클래스(.으로 구분해준다)
    insta = soup.select('.v1Nh3.kIKUG._bz0w')

    # 이미지 하나만 가져올 게 아니라 여러 개를 가져올 것이므로 반복문
    for i in insta:
        print('https://www.instagram.com' + i.a['href'])
        imgUrl = i.select_one('.KL4Bh').img['src']
        imglist.append(imgUrl)
        imglist = list(set(imglist))
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        insta = soup.select('.v1Nh3.kIKUG._bz0w')

    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(3)

n = 0

for i in range(0, M):
    print(n)
    image_url = imglist[n]
    resp = requests.get(image_url, stream=True)
    local_file = open('./img/' + hashTag + str(n) + '.jpg', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)

    n += 1
    del resp

driver.close()