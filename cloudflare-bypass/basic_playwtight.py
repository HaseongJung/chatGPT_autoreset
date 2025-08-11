import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    url = "https://chat.openai.com"  # replace with target URL
    page.goto(url, timeout=60000)
    html = page.content()


    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html)
        time.sleep(5)  # wait for the login page to load

        page.click("text=로그인")
        time.sleep(5)  # wait for the login page to load

        browser.close()