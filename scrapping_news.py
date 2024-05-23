from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import re
import warnings
from bs4 import GuessedAtParserWarning

warnings.filterwarnings('ignore', category=GuessedAtParserWarning)

def scrap_cnn(url):
    document = requests.get(url).text
    dom = BeautifulSoup(document, "html")

    title = dom.select_one("title")
    title = title.text
    if not("FOTO:" in title or "VIDEO:" in title or "INFOGRAFIS:" in title) :
        article_div = dom.select_one("div.detail-text")
        snippet_element = article_div.select("p")
        
        data = {
            "url" : url, 
            "title" : title,
            "content" : ""
            }
        text = ''
        for content in snippet_element:
            current = content.text
            current = re.sub(r'[^\x00-\x7F]+',' ', current)
            if current.strip() not in ["ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT", ""]:
                if current.strip().endswith("."):
                    text += current + " "
                else:
                    text += current
        data["content"] = text.strip()
        return data
    

def scrap_detik(url):
    document = requests.get(url).text
    dom = BeautifulSoup(document, "html")
    
    title = dom.select_one("title")
    title = title.text
    
    data = {
            "url" : url, 
            "title" : title,
            "content" : ""
            }
    
    article_div = dom.select_one("div.detail__body-text")
    snippet_element = article_div.select("p")
    text = ''
    for content in snippet_element:
        current = content.text
        current = re.sub(r'[^\x00-\x7F]+',' ', current)
        if current.strip() not in ["ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT", "", "Simak selengkapnya di sini."]:
            if current.strip().endswith("."):
                text += current + " "
            else:
                text += current
        
    data["content"] = text.strip()
    return data


def scrap_kompas(url):
    document = requests.get(url).text
    dom = BeautifulSoup(document, "html")

    title = dom.select_one("title")
    title = title.text
    data = {
            "url" : url, 
            "title" : title,
            "content" : ""
            }
    article_div = dom.select_one("div.read__content")
    snippet_element = article_div.select("p")
    text = ''
    for content in snippet_element:
        current = content.text
        current = re.sub(r'[^\x00-\x7F]+',' ', current)
        if current.strip() not in ["ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT", "", "Simak selengkapnya di sini."] and not current.strip().startswith("Baca juga:"):
            if current.strip().endswith("."):
                text += current + " "
            else:
                text += current
    data["content"] = text.strip()
    return data


def scrap_antara(url):
    document = requests.get(url).text
    dom = BeautifulSoup(document, "html")

    title = dom.select_one("div.wrap__article-detail-title")
    title = title.text
    data = {
            "url" : url, 
            "title" : title,
            "content" : ""
            }
    article_div = dom.select_one("div.post-content")
    text = ''
    for content in article_div:
        current = content.text
        current = re.sub(r'[^\x00-\x7F]+',' ', current)
        if current.strip() not in ["ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT", "", "Simak selengkapnya di sini."] and not current.strip().startswith("Baca juga:") and not current.strip().startswith("Pewarta:") and not current.strip().startswith("MulyaEditor:") and not current.strip().startswith("Copyright"):
            if current.strip().endswith("."):
                text += current.strip() + " "
            else:
                text += current.strip()
    text = text.replace("Selengkapnya disini.", "")
    data["content"] = text.strip()
    return data
    

def scrap_narasi(url):
    driver = webdriver.Chrome()

    driver.get(url)
    title = driver.find_element(By.TAG_NAME, "h1").text.strip()
    article_div = driver.find_element(By.CSS_SELECTOR, "p.desc-article")
    snippet_element = article_div.find_elements(By.CSS_SELECTOR, "p")

    data = {
            "url" : url, 
            "title" : title,
            "content" : ""
            }
    text = ""
    for content in snippet_element:
        current = content.text
        if current.strip() not in ["ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT", ""]:
            text += current + " "

    data["content"] = text.strip()
    return data
    

def scrap_liputan6(url):
    document = requests.get(url).text
    dom = BeautifulSoup(document, "html")

    title = dom.select_one("title")
    title = title.text
    data = {
            "url" : url, 
            "title" : title,
            "content" : ""
            }
    article_div = dom.select_one("div.article-content-body__item-content")
    snippet_element = article_div.select("p")
    text = ''
    for content in snippet_element:
        current = content.text
        current = re.sub(r'[^\x00-\x7F]+',' ', current)
        if current.strip() not in ["ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT", "", "Simak selengkapnya di sini."] and not current.strip().startswith("Baca juga:"):
            if current.strip().endswith("."):
                text += current + " "
            else:
                text += current
    data["content"] = text.strip()
    return data


def scrap_cnbc(url):
    document = requests.get(url).text
    dom = BeautifulSoup(document, "html")

    title = dom.select_one("title")
    title = title.text
    data = {
            "url" : url, 
            "title" : title,
            "content" : ""
            }
    article_div = dom.select_one("div.detail_text")
    snippet_element = article_div.select("p")
    text = ''
    for content in snippet_element:
        current = content.text
        current = re.sub(r'[^\x00-\x7F]+',' ', current)
        if current.strip() not in ["ADVERTISEMENT", "SCROLL TO RESUME CONTENT", "", "Simak selengkapnya di sini."] and not current.strip().startswith("Baca juga:"):
            if current.strip().endswith("."):
                text += current + " "
            else:
                text += current
    data["content"] = text.strip()
    return data


def get_news(url: str):
    if "www.cnbcindonesia.com" in url:
        return scrap_cnbc(url)
    elif "www.liputan6.com" in url:
        return scrap_liputan6(url)
    elif "narasi.tv" in url:
        return scrap_narasi(url)
    elif "www.antaranews.com" in url:
        return scrap_antara(url)
    elif "news.detik.com" in url:
        return scrap_detik(url)
    elif "www.cnnindonesia.com" in url:
        return scrap_cnn(url)
    elif "kompas.com" in url :
        return scrap_kompas(url)
    else :
        return "Berita tidak bisa didapat dari link yang diberikan. Silakan masukkan teks berita secara manual."