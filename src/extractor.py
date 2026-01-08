import requests
from bs4 import BeautifulSoup

def extract_article(url):
    try:
        page=requests.get(url,timeout=10)
        if page.status_code != 200:
            return ""
    except:
        return ""

    soup=BeautifulSoup(page.text,"html.parser")

    content=[]
    articles=soup.find_all("article")

    for article in articles:
        for tag in article.find_all(["h1","h2","h3","p"]):
            text=tag.get_text(strip=True)
            if text:
                content.append(text)

    return "\n".join(content)
