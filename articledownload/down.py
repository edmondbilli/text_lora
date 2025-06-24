import requests
from bs4 import BeautifulSoup
import os, time

def get_article_links(page_url):
    resp = requests.get(page_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Select <a> tags with data-rel="slide-1"
    links = [a['href'] for a in soup.select('a[data-rel="slide-1"]')]
    return links

def get_article_text(article_url):
    resp = requests.get(article_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    content = soup.select_one('div.entry-content')
    if content:
        cnt = content.get_text(strip=True)
        cnt = cnt.split("Click on a heart to thank the author of this story")[0]
    else:
        cnt = ""
    time.sleep(1)  # Be polite and avoid overwhelming the server
    return cnt

def crawl_articles(start_page=2, end_page=5):
    os.makedirs('articles', exist_ok=True)
    for page in range(start_page, end_page + 1):
        page_url = f'https://marriageheat.com/?fwp_paged={page}'
        print(f'Crawling page: {page_url}')
        article_links = get_article_links(page_url)
        for idx, link in enumerate(article_links):
            print(f'Fetching article: {link}')
            text = get_article_text(link)
            # Save each article to a separate file
            filename = f'articles/page{page}_article{idx+1}_'+ link.rsplit("/")[-2] +'.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f'Saved: {filename}')

if __name__ == '__main__':
    crawl_articles(61, 100)