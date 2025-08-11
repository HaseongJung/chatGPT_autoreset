from seleniumbase import SB
import pyautogui as pg
import time
import random as rd


# 옵션
# 창 최대화
# --start-maximized

ID = 'edu7@scopelabs.site'
chatGPT_PW = 'scopelabs28@@'
whois_PW = 'scopelabs2023!'



def get_authentication_code(sb, ID, whois_PW):
        # 새 탭 열기
    pg.hotkey('ctrl', 't')
    sb.sleep(rd.uniform(0, 1))

    # 새 탭에서 이메일 확인 페지 열기
    email_url = "https://desk.go.whoisworks.com/"
    # sb.oepn_new_window(email_url)
    sb.switch_to_window(1)
    sb.open(email_url)
    sb.sleep(rd.uniform(2, 3))

    

    # 후이즈 로그인
    sb.type('#account', ID, timeout=10)
    sb.type('#password', whois_PW, timeout=10)
    sb.click('#loginForm > button', timeout=10)
    sb.sleep(rd.uniform(2, 3))


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

    # 인증 코드 추출
    try:
        auth_code_elements = sb.find_elements('#mail_contents p')
        authentication_code_element = sb.find_element('div > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(3) > td > p:nth-child(2)')
        authentication_code = authentication_code_element.text.strip()
        print("인증 코드:", authentication_code)
    except Exception as e:
        print("인증 코드를 찾을 수 없습니다:", e)
        # exit(1)
    
    # 인증 코드 입력
    pg.hotkey('ctrl', 'w')  # 새 탭 닫기

    return authentication_code


def main():

    with SB(uc=True, incognito=True, test=True) as sb:
        # url = "https://auth.openai.com/log-in"
        charGPT_url = 'https://chatgpt.com/'
        sb.uc_open_with_reconnect(charGPT_url, rd.uniform(2, 3))
        # sb.uc_gui_click_captcha()
        # sb.uc_gui_handle_captcha()
        sb.maximize_window()
        sb.sleep(rd.uniform(1, 2))


        # 로그인 버튼 클릭
        try:
            current_url = sb.get_current_url()
            login_button = pg.locateOnScreen('./images/login_button_01.png', confidence=0.6)
            sb.sleep(rd.uniform(1, 2))
            pg.moveTo(login_button, duration=rd.uniform(0, 1))
            pg.click()
            time.sleep(rd.uniform(1, 2))
            # 로그인 버튼 클릭 후 URL 확인
            if (sb.get_current_url() != current_url):
                print("로그인 버튼 클릭 성공")
            else:
                pg.click(login_button) 
            sb.sleep(rd.uniform(2, 3))
        except Exception as e:

            print("로그인 버튼을 찾을 수 없습니다:", e)


        # 이메일 주소 입력
        pg.write(ID)  
        sb.sleep(rd.uniform(1, 2))
        # enter 키 입력
        pg.press("enter")
        sb.sleep(rd.uniform(2, 3))

        # 비밀번호 입력
        pg.write(chatGPT_PW)
        sb.sleep(rd.uniform(1, 2))
        pg.press("enter")
        sb.sleep(rd.uniform(2, 3))

        # 인증 버튼 클릭
        try:
            verification_button = pg.locateOnScreen('./images/verification_button.png', confidence=0.6)
            sb.sleep(rd.uniform(1, 2))
            pg.moveTo(verification_button, duration=rd.uniform(0, 1))  # 마우스 이동
            pg.click(verification_button)
            sb.sleep(rd.uniform(1, 2))
        except Exception as e:
            print("인증 버튼을 찾을 수 없습니다:", e)
            # exit(1)

        # 검증 방법 '이메일' 선택
        try:
            email_verification_button = pg.locateOnScreen('./images/verification_select_email.png', confidence=0.6)
            sb.sleep(rd.uniform(1, 2))
            pg.moveTo(email_verification_button, duration=rd.uniform(0, 1))  # 마우스 이동
            pg.click(email_verification_button)
            sb.sleep(rd.uniform(1, 2))
        except Exception as e:
            print("이메일 인증 버튼을 찾을 수 없습니다:", e)
            # exit(1)

        sb.sleep(rd.uniform(0, 1))

        try:
            authentication_code = get_authentication_code(sb, ID, whois_PW)
        # print("인증 코드:", authentication_code)
        except Exception as e:
            print("인증 코드를 가져오는 데 실패했습니다:", e)
            # exit(1)

        # # '계속' 버튼 클릭
        # # continue_button_point = (960, 424)
        # # pyautogui.moveTo(continue_button_point)
        # pg.click()

        time.sleep(5)




        # sb.assert_text("Username", '[for="user_login"]', timeout=3)
        # sb.assert_element('label[for="user_login"]')
        # sb.highlight('button:contains("Sign in")')
        # sb.highlight('h1:contains("GitLab.com")')
        # sb.post_message("SeleniumBase wasn't detected", duration=4)



if __name__ == "__main__":
    main()

