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


def scrape_nature_article(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get title
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Get description
    desc_tag = soup.find(name='meta', attrs={'name': 'description'})
    description = desc_tag['content'].strip() if desc_tag else "No description found"

    # Get body

    return {"title": title, "description": description}


def response_to_html(response):
    content = response.content
    with open('source.html', 'wb') as file:  # using 'wb' to save the content in binary mode
        file.write(content)
        print('Content saved.')


def main() -> None:
    try:
        url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3'
        response = get_response(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles_tag = soup.findAll(name='article')
        print('Total articles: ', len(articles_tag))

        for article in articles_tag:
            span_tag = article.find(name='span', attrs={'data-test': 'article.type'})

            if span_tag and span_tag.get_text(strip=True) == "News":
                article_link = article.find(name='a', attrs={'data-track-action': 'view article'})
                if article_link:
                    article_url = article_link.get('href')
                    print(article_url)


    except InvalidPageException as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
