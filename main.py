from bs4 import BeautifulSoup
import requests
import re


articles_list = []
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
HEADERS = {
    'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.'
              '2.528119004.1639149415; _gid=GA1.2.512914915.'
              '1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru;'
              ' _ym_isad=2; __gads=ID=87f529752d2e0de1-'
              '221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-mobile': '?0'
}


def text_article():
    url = 'https://habr.com/ru/all/'
    baseurl = 'https://habr.com'
    page = requests.get(url, headers=HEADERS).content
    soup = BeautifulSoup(page, "html.parser")
    articles = soup.findAll('article', class_="tm-articles-list__item")

    for data in articles:
        tag_list = []
        name = data.find('a', class_="tm-article-snippet__title-link").text
        tags = data.findAll('a', class_='tm-article-snippet__hubs-item-link')
        for tag in tags:
            tag_list.append(tag.text.replace('*','').strip())
        try:
            texts = data.find('div', class_="article-formatted-body article-formatted-body "
                                            "article-formatted-body_version-2").text.strip().\
                replace('\n','').replace('\xa0','').replace('\r','')
        except:
            texts = data.find('div', class_="article-formatted-body article-formatted-body "
                                            "article-formatted-body_version-1").text.strip().\
                replace('\n','').replace('\xa0','').replace('\r','')
        dates = data.find('time')['datetime']
        links = baseurl + data.find('a', class_='tm-article-snippet__title-link')['href']
        articles_list.append([[name], [dates], tag_list, [texts], [links]])


def search_words():
    for search_string in KEYWORDS:
        for n in range(len(articles_list)):
            names = "".join(articles_list[n][0])
            tags = "".join(articles_list[n][2])
            texts = "".join(articles_list[n][3])
            if re.findall(f'{search_string}', names, re.IGNORECASE) or re.findall(f'{search_string}',
                    tags, re.IGNORECASE) or re.findall(f'{search_string}', texts, re.IGNORECASE):
                print(f"{articles_list[n][1]}\n{articles_list[n][0]}\n{articles_list[n][-1]}\n")


if __name__ == "__main__":
    text_article()
    search_words()


