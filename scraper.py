import requests
from bs4 import BeautifulSoup


class InvalidPageException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def read_url() -> str:
    url = input('Intput thr URL: \n')
    if 'nature' not in url and 'articles' not in url:
        raise InvalidPageException('Invalid page!')
    return url


def get_response(url: str, headers: dict = None):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise InvalidPageException('Invalid page!')
    return response


def scrape_nature_article(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get title
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Get description
    desc_tag = soup.find('meta', {'name': 'description'})
    description = desc_tag['content'].strip() if desc_tag else "No description found"

    return {"title": title, "description": description}


def main() -> None:
    try:
        url = read_url()
        response = get_response(url)
        nature_article = scrape_nature_article(response)
        print(nature_article)
    except InvalidPageException as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
