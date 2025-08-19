import os
import time
from dotenv import load_dotenv

from seleniumbase import SB
import pyautogui as pg

from utils.pyautoGUI_helper import wait_and_find_element, find_and_click
from whois import get_authentication_code



# load .env
load_dotenv()

ID = os.getenv("ID")
chatGPT_PW = os.getenv("chatGPT_PW")
WHOIS_PW = os.getenv("WHOIS_PW")
NEW_GPT_PW = os.getenv("NEW_GPT_PW")




    
def main():
    with SB(uc=True, incognito=True, test=True, window_size='1920, 1080', maximize=True) as sb:

        sb.open("https://chatgpt.com/")
        sb.uc_gui_handle_captcha()

        # 로그인 버튼 클릭
        find_and_click('./images/login.png', timeout=3)


        # 이메일 input요소 클릭
        find_and_click('./images/email_input.png', timeout=3)

        # 이메일 주소 입력
        try:
            pg.write(ID)
            pg.press("enter")
        except Exception as e:
            print("이메일 입력 중 오류 발생:", e)


        # '비밀번호를 잊으셨나요?' 링크 클릭
        find_and_click('./images/forgot_password.png')

        # '계속' 버튼 클릭
        find_and_click('./images/continue.png')


        # 인증 코드 입력
        try:
            auth_code = get_authentication_code(sb, ID, WHOIS_PW)
            if auth_code:
                # 코드 input 요소 클릭
                code_input_element = wait_and_find_element('./images/code_input.png')
                pg.click(code_input_element)
                # 인증 코드 입력
                pg.write(auth_code)
                pg.press("enter")
            else:
                print("인증 코드를 받지 못했습니다.")
        except Exception as e:
            print("인증 코드 입력 중 오류 발생:", e)

        # 비밀번호 변경
        try:
            time.sleep(2)
            pg.write(NEW_GPT_PW)
            pg.press("tab")
            pg.press("tab")
            pg.write(NEW_GPT_PW)
            pg.press("enter")
        except Exception as e:
            print("비밀번호 변경 중 오류 발생:", e)


        print('비밀번호 변경 완료')


if __name__ == "__main__":
    main()