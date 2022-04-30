import requests as requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os


def get_response(url, page_num=None):
    if page_num:
        request = requests.get(url, params={'page': page_num})
        print(request.url)
        if request:
            return BeautifulSoup(request.content, 'html.parser')
        return False
    else:
        request = requests.get(url)
        if request:
            return BeautifulSoup(request.content, 'html.parser')
        return False


number_of_pages = int(input())
article_type = input()
link = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
for j in range(1, number_of_pages + 1):
    soup = get_response(link, j)
    if soup:
        articles = soup.find_all('article')
        links = []
        articles_names = []
        saved_articles = []
        for article in articles:
            if article.find('span', "c-meta__type").text == article_type:
                links.append(article.h3.a.get('href'))
                articles_names.append(article.h3.a.text)
        os.mkdir(f'Page_{j}')
        os.chdir(f'Page_{j}')
        for i in range(len(links)):
            url = urljoin(link, links[i])
            new_r = get_response(url)
            template = r'[!"#$%&\'()*+,-./:;<=>\?@\[\\\]^_`{|}~]'
            file_name = re.sub(template, '', articles_names[i]).replace(" ", "_") + ".txt"
            with open(file_name, 'wb') as file:
                if new_r:
                    string = new_r.find('div', {'class': "c-article-body u-clearfix"}).get_text(separator='').replace('\n', '')
                    print(string)
                    file.write(string.encode('UTF-8'))
                    # file.write(re.sub(r'\s+', ' ', string.text).encode('UTF-8'))
                    saved_articles.append(file_name)
        print(f"Saved articles:\n{saved_articles}")
        os.chdir(os.path.dirname(os.getcwd()))
    else:
        print("Invalid link")

