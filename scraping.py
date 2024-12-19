import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import time
import json

s = time.time()

async def links():
    hrefs = []
    url = "https://haberglobal.com.tr/gundem"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        soup = BeautifulSoup(await response.text(), "html.parser")
        links = soup.find_all("a")
        for link in links:
            href = link["href"]
            if href.startswith("https://haberglobal.com.tr/gundem") and len(href) > 35:
                hrefs.append(href)
        return hrefs 

async def get_info(url):
    url = url
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        soup = BeautifulSoup(await response.text(), "html.parser")

        title = soup.find("header", class_ = "post-detail-header").text
        news = soup.find("h2").text
        datetime = soup.find("div", class_ = "post-dates").text
        return {
            "Title": title.strip() if title else "None",
            "News": news.strip() if news else "None",
            "Datetime": datetime.strip() if datetime else "None"
        }

async def main():
    hrefs = await links()
    tasks = []
    for count, link in enumerate(hrefs, start=1):
        print(f"{count} info added")
        tasks.append(get_info(link))

    results = await asyncio.gather(*tasks)
    with open ("habergloobalnews.json", "w", encoding="utf8") as f:
        f.write(json.dumps(results, indent=4, ensure_ascii=False))

asyncio.run(main())
e = time.time()
print(e-s)