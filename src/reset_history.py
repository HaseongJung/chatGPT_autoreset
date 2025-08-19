import os
import time
import random as rd
from dotenv import load_dotenv

from seleniumbase import SB
import pyautogui as pg

from utils.pyautoGUI_helper import wait_and_find_element, find_and_click
from src.whois import get_authentication_code





# load .env
load_dotenv()

ID = os.getenv("ID")
GPT_PW = os.getenv("GPT_PW")
WHOIS_PW = os.getenv("WHOIS_PW")
NEW_PW = os.getenv("NEW_PW")





def login_chatGPT(sb, ID, chatGPT_PW, whois_PW):
    find_and_click('./images/login.png', timeout=3)   # 로그인 버튼 클릭
    find_and_click('./images/email_input.png', timeout=2, confidence=0.5) # 이메일 input요소 클릭
    
    # 이메일 주소 입력
    try:
        pg.write(ID)
        pg.press("enter")
    except Exception as e:
        print("이메일 입력 중 오류 발생:", e)

    try:
        # 비밀번호 입력
        sb.wait_for_element_visible('//input[@type="password"]', by='xpath', timeout=10)
        pg.write(chatGPT_PW)
        # enter 키 입력 
        sb.sleep(rd.uniform(0.3, 0.5))
        pg.press("enter")
    except Exception as e:
        print("비밀번호 입력 중 오류 발생:", e)


    find_and_click('./images/other_verification.png')    # 검증 - "다른 방법도 있어요" 클릭
    find_and_click('./images/email.png')    # 검증 방법 '이메일' 선택

    # 인증 코드 입력
    authentication_code = get_authentication_code(sb, ID, whois_PW)
    if (authentication_code):
        try:
            pg.write(authentication_code)
            pg.press("enter")

        except Exception as e:
            print("인증 코드 입력 중 오류 발생:", e)


def reset_memory():
    find_and_click('./images/personal_settings.png', duration=1) # '개인맞춤설정' 카테고리 클릭
    find_and_click('./images/management.png', duration=1, confidence=0.9)   # '메모리 관리' 버튼 클릭    
    find_and_click('./images/delete_all.png', duration=1)   # '모두 삭제' 버튼 클릭
    find_and_click('./images/clear_memory.png', duration=1) # '메모리 지우기' 버튼 클릭
    print("메모리 초기화 완료")

def clear_history():
    find_and_click('./images/data_control.png', duration=1) # '데이터 제어' 카테고리 클릭
    find_and_click('./images/delete_all.png', duration=1) # '모두 삭제' 버튼 클릭
    find_and_click('./images/delete.png', duration=1) # '삭제' 버튼 클릭 (여러 개가 있을 경우 처리)
    print("채팅 기록 삭제 완료")

def reset_chatGPT(sb):
    time.sleep(5)
    find_and_click('./images/workspace.png') # 워크스페이스 선택
    find_and_click('./images/profile.png', duration=1) # 프로필 버튼 클릭
    find_and_click('./images/settings.png', duration=1) # 설정 버튼 클릭

    # 메모리 초기화
    reset_memory()

    # 닫기
    find_and_click('./images/close.png', duration=1)

    # 채팅 기록 삭제
    clear_history()

def main():
    with SB(uc=True, incognito=True, test=True, window_size='1920, 1080', maximize=True) as sb:

        sb.open("https://chatgpt.com/")
        sb.uc_gui_handle_captcha()

        login_chatGPT(sb, ID=ID, chatGPT_PW=GPT_PW, whois_PW=WHOIS_PW)

        reset_chatGPT(sb)

if __name__ == "__main__":
    main()
