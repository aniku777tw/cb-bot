from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

cache = {}

def get_cache():
    return cache

def set_cache(data, code):
    cache[code + datetime.today()] = data

def fetch_convertbond_info_with_cache(code: str):
    if code in cache:
        print("從快取讀取")
        return cache[code + datetime.today()]
    return None

def fetch_convertbond_info(code: str) -> list:
    """抓取指定代碼的所有 <tr> 標籤資訊"""
    url = f"https://thefew.tw/quote/{code}"

    # 設置 Selenium 的選項，使其運行在無頭模式（不顯示瀏覽器）
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "/usr/bin/google-chrome"
    
    # 初始化 Chrome WebDriver
    driver = webdriver.Chrome(options=options)

    try:
        # 載入網頁
        driver.get(url)
        time.sleep(3)  # 等待頁面加載完成

        # 使用 BeautifulSoup 解析網頁源碼
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 抓取所有的 <tr> 標籤
        rows = soup.find_all('tr')

        # 存儲每一行的文字內容
        data = []
        for row in rows:
            row_text = [cell.text.strip() for cell in row.find_all(['td', 'th'])]  # 獲取 <td> 或 <th> 標籤的文字
            if row_text:
                data.append(row_text)
        # 只保留前 10 行資料
        important_info = [
            ['可轉債名稱', data[0][1]],  # 中砂一
            ['轉換價值', data[5][1]],  # 92.99
            ['轉換溢價率', data[8][1]],  # 21.6%
            ['發行價格', data[12][1]],  # 118.38
            ['CBAS 權利金（百元報價）', data[6][1]],  # 5.94
            ['最新 CB 收盤價', data[4][1]],  # 113.1(0%)
            ['最新股票收盤價', data[9][1]],  # 268.0(0%)
            ['發行總額(百萬)', data[13][1]],  # 1000
            ['發行日', data[16][1]],  # 2024-06-24
            ['到期日', data[17][1]],  # 2029-06-24
        ]

        return data[:-3]

        

    except Exception as e:
        return {"error": str(e)}

    finally:
        # 關閉瀏覽器
        driver.quit()
        # 測試爬取代碼為 15601 的可轉債資料

