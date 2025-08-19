from seleniumbase import SB
import pyautogui as pg
import time
import random as rd
from bs4 import BeautifulSoup as bs4
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

ID = os.getenv("ID")
GPT = os.getenv("GPT_PW")
WHOIS_PW = os.getenv("WHOIS_PW")


def get_authentication_code(sb, ID, whois_PW):
    
    # 새 탭 열기
    pg.hotkey('ctrl', 't')
    sb.sleep(rd.uniform(0, 1))

    # 새 탭에서 이메일 확인 페이지 열기
    email_url = "https://desk.go.whoisworks.com/"
    # sb.oepn_new_window(email_url)
    sb.switch_to_window(1)
    sb.open(email_url)


    # 후이즈 로그인
    sb.type('#account', ID, timeout=10)
    sb.type('#password', whois_PW, timeout=10)
    sb.click('#loginForm > button', timeout=10)
    sb.sleep(rd.uniform(2, 3))

    # 새로 고침
    print("Waiting for new mail...(5 sec)")
    time.sleep(5)
    sb.refresh()

    # 이메일 인증 코드 찾기
    try:
        received_mails =  sb.find_elements('div.text-truncate')
        last_mail = received_mails[0]
        # sb.sleep(rd.uniform(1, 2))
        # 마지막 이메일 클릭
        last_mail.click()
        sb.sleep(rd.uniform(2, 3))
    except Exception as e:
        print("이메일을 찾을 수 없습니다:", e)
        # exit(1)

    # 3번째 탭으로 이동
    sb.switch_to_window(2)

    # 인증코드 추출
    try:
        html = sb.driver.page_source
        soup = bs4(html, "html.parser")

        auth_code = soup.get_text().replace('\n', '').split(':')[3].lstrip().split(' ')[0]
        print("인증 코드:", auth_code)

    except Exception as e:
        print("인증 코드 추출 실패:", e)
        auth_code = None

    # 현재 탭 닫기
    sb.sleep(rd.uniform(1, 2))
    sb.driver.close()
    sb.switch_to_window(1)
    # 현재 탭 닫기
    sb.sleep(rd.uniform(1, 2))
    sb.driver.close()    
    sb.switch_to_window(0)


    return auth_code