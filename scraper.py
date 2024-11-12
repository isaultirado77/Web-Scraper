import requests
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


def scrape_article_links(url: str) -> list:
    response = get_response(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_links = list()

    articles_tag = soup.findAll(name='article')

    for article in articles_tag:
        span_tag = article.find(name='span', attrs={'data-test': 'article.type'})

        if span_tag and span_tag.get_text(strip=True) == "News":
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


def data_to_txt(data_list: list) -> None:
    if data_list is None:
        return

    for data in data_list:
        file_name = f'{data['title']}.txt'
        with open(file_name, 'w') as file:
            file.write(data['body'])
    print(f'Saved articles: {''.join([f'{item['title']}.txt' for item in data_list])}')


def response_to_html(response):
    content = response.content
    with open('source.html', 'wb') as file:  # using 'wb' to save the content in binary mode
        file.write(content)
        print('Content saved.')


def main() -> None:
    try:
        url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3'
        links = scrape_article_links(url)
        data = []
        for link in links:
            data.append(scrape_nature_article(link))
        data_to_txt(data)

    except InvalidPageException as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
