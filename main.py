import requests
from bs4 import BeautifulSoup
import time
import re


def fetch_domains():
    url = "https://dns.aizhan.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            domain_links = []
            # 仅选取 href 中包含 "/cha/" 的链接
            for a in soup.find_all("a", href=True):
                href = a['href']
                if "/cha/" in href:
                    text = a.get_text().strip()
                    # 使用正则过滤符合域名格式（包含至少一个点）的文本
                    if re.match(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$", text):
                        domain_links.append(text)
            return domain_links
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"请求异常：{e}")
    return []


def get_interval():
    while True:
        user_input = input("请输入获取间隔时间（秒），直接回车使用默认60秒：").strip()
        if user_input == "":
            return 60
        try:
            interval = int(user_input)
            if interval > 0:
                return interval
            else:
                print("请输入大于0的整数。")
        except ValueError:
            print("输入无效，请输入一个整数。")


if __name__ == "__main__":
    interval = get_interval()
    print(f"设置获取间隔为 {interval} 秒。")

    while True:
        domains = fetch_domains()
        if domains:
            for domain in domains:
                print(domain)
        else:
            print("未能获取到域名数据。")
        print(f"等待 {interval} 秒后再次获取...\n")
        time.sleep(interval)
