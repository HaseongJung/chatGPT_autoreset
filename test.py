# import asyncio
# from playwright.async_api import async_playwright
# import json

# async def save_cookies():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         context = await browser.new_context()
#         page = await context.new_page()

#         # await page.goto("https://chat.openai.com/")
#         await page.goto("https://chat.openai.com/auth/login")

#         print("로그인 후 Enter 키를 누르세요...")
#         input()  # 수동 로그인 대기

#         cookies = await context.cookies()
#         with open("cookies.json", "w") as f:
#             json.dump(cookies, f, indent=2)

#         await browser.close()

# asyncio.run(save_cookies())


import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # 크롬에서 추출한 쿠키 불러오기
        with open('./cookie/cookie.json', 'r') as f:
            raw_cookies = json.load(f)

        # Playwright 형식으로 변환 (필요 시)
        cookies = [
            {
                "name": c["name"],
                "value": c["value"],
                "domain": c["domain"],
                "path": c.get("path", "/"),
                "expires": float(c.get("expirationDate", -1)),
                "httpOnly": c.get("httpOnly", False),
                "secure": c.get("secure", False),
                "sameSite": "Lax",  # 또는 None, Strict
            }
            for c in raw_cookies
        ]

        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto("https://chat.openai.com")

        await page.wait_for_timeout(10000)

        await browser.close()

asyncio.run(main())