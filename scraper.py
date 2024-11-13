import string
import requests
import os
from bs4 import BeautifulSoup
from http import HTTPStatus


class InvalidPageException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def read_url() -> str:
    url = input('Intput thr URL: \n')
    return url


def get_response(url: str, headers: dict = None):
    response = requests.get(url, headers=headers)
    if response.status_code != HTTPStatus.OK:
        raise InvalidPageException(f'The URL returned {response.status_code}')
    return response


def scrape_articles_links(url: str, article_type: str) -> list:
    response = get_response(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_links = list()

    articles_tag = soup.findAll(name='article')

    for article in articles_tag:
        span_tag = article.find(name='span', attrs={'data-test': 'article.type'})

        if span_tag and span_tag.get_text(strip=True) == article_type:
            article_link = article.find(name='a', attrs={'data-track-action': 'view article'})
            if article_link:
                article_url = article_link.get('href')
                article_links.append('https://www.nature.com' + article_url)
    return article_links


def scrape_nature_article(url: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get title
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Get description
    desc_tag = soup.find(name='meta', attrs={'name': 'description'})
    description = desc_tag['content'].strip() if desc_tag else "No description found"

    # Get body
    body_tag = soup.find(name='p', attrs={"class": "article__teaser"})
    body = body_tag.get_text(strip=True)

    return {"title": title, "description": description, 'body': body}


def remove_punctuation(text: str) -> str:
    for symbol in string.punctuation:
        if symbol in text:
            text.replace(symbol, '')
    return text


def data_to_txt(data_list: list, N: int) -> None:
    folder_name = f'Page_{N}'
    os.makedirs(folder_name, exist_ok=True)

    if data_list:
        for data in data_list:
            title = remove_punctuation(data['title']).replace(' ', '_')
            body_text = data['body']
            file_path = os.path.join(folder_name, f'{title}.txt')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(body_text)
    else:
        print('No data found.')


def response_to_html(response):
    content = response.content
    with open('source.html', 'wb') as file:  # using 'wb' to save the content in binary mode
        file.write(content)
        print('Content saved.')


def get_next_page_urls(url: str, narticles: int):
    next_urls = [url]
    for _ in range(narticles):
        response = requests.get(next_urls[-1])
        soup = BeautifulSoup(response.content, 'html.parser')

        next_tag = soup.find(name='li',
                             attrs={'data-page': 'next', 'class': 'c-pagination__item', 'data-test': 'page-next'})
        if next_tag:
            url_tag = next_tag.find(name='a', attrs={'class': 'c-pagination__link'})
            if url_tag:
                next_url = url_tag.get('href')
                next_urls.append('https://www.nature.com' + next_url)
    return next_urls


def get_articles_link_per_page(pages_urls: list, article_type: str):
    articles_links_per_page = []
    for url in pages_urls:
        articles_link = scrape_articles_links(url, article_type)
        articles_links_per_page.append(articles_link)
    return articles_links_per_page


def main() -> None:
    try:
        url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
        narticles = int(input())
        article_type = input()
        next_page_urls = get_next_page_urls(url, narticles)
        articles_links_per_page = get_articles_link_per_page(next_page_urls, article_type)

    except InvalidPageException as e:
        print(f'Error: {e}')
    except ValueError:
        print('Error: Enter a valid number. ')


if __name__ == '__main__':
    main()
