import re, os, time
import json
import requests
from bs4 import BeautifulSoup

DOMAINS = ['politica', 'social', 'cultura', 'regionale', 'economic-intern', 'justitie','educatie-stiinta','eveniment','sanatate','mediu', 'politica-externa', 'romania-in-lume', 'stiintatehnica', 'economic-extern', 'mondorama', 'life', 'planeta']

def extract_article_links_from_page(page_url, domain):
    page_article_urls = []
    reqs = requests.get(page_url)
    if reqs.status_code != 200:
        return []
    page_soup = BeautifulSoup(reqs.text, 'html.parser')

    for _url in page_soup.find("div", class_="wrapper_news_articles wrapper_on_category_page").find_all('a'):
        if re.findall(r'\d{4}\/\d{2}\/\d{2}', _url.get('href')) and "--" in _url.get('href'):
            link = str(_url)[9:]
            link = link[:link.index('"')]
            if link not in page_article_urls:
                page_article_urls.append(link)

    return page_article_urls


def download_article(url):
    try:
        time.sleep(1)
        #print(f'Crawling article {url}')
        _reqs = requests.get(url)
        if _reqs.status_code != 200:
            raise Exception(f"Non 200 status code : {_reqs.status_code}")
        article_soup = BeautifulSoup(_reqs.text, 'html.parser')
        article_title = str(article_soup.find_all("div", class_="details_news")[0].contents[0].next)
        article_date_time = str(article_soup.find_all("div", class_="details_news")[0].contents[1].next.next)
        _article_content = article_soup.find_all("div", class_="description_articol")[0].text
        article_data = {'title': article_title, 'content': _article_content,
                        'date_time': article_date_time, 'url': url}
        return article_data
    except Exception as exc:
        print(exc)
        return None

def update_category(category, max_articles=1000000, save_steps=50, max_errors=10, file_path=""):
    # load category articles
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf8") as f:
            data = json.load(f)
    else:
        data = {}

    step, errors = 0, 0

    # estimate next page
    estimated_page = max(0, int(len(data)/10)-2)
    print(f"Estimating page {estimated_page}")

    # start iteration
    for i in range(estimated_page, 10000):
        page_url = f'https://www.agerpres.ro/{category}/page/{i}'
        links = extract_article_links_from_page(page_url, category)
        print(f"\tExtracted from page {page_url} {len(links)} links")
        if len(links) == 0:
            print("No more links or smth is wrong.")
            return

        for link in links:
            if link not in data:
                try:
                    data[link] = download_article(f'https://www.agerpres.ro{link}')
                    print(f"{link} done, {len(data)} total news in {category}")
                    step += 1
                    errors = 0
                    if step >= save_steps:
                        step = 0
                        print(f"Saving {category} ... ")
                        with open(file_path, 'w', encoding="utf8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                    if len(data)>max_articles:
                        print(f"Reached max limit for articles ({max_articles}), exiting ...")
                        with open(file_path, 'w', encoding="utf8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        return

                except Exception as ex:
                    print(f"Exception : {str(ex)}")
                    errors += 1
                    if errors >= max_errors:
                        print("Too many errors, exiting...")
                        return

import sys

if len(sys.argv) <= 1:
    category = DOMAINS[0]
else:
    category = DOMAINS[int(sys.argv[1])]
    print(f"Doing manual category: {category} ...")

update_category(category, file_path=f'raw_{category}.json')
