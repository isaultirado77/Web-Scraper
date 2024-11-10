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


def get_title_description_article(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get title
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Get description
    desc_tag = soup.find('meta', {'name': 'description'})
    description = desc_tag['content'].strip() if desc_tag else "No description found"

    return {"title": title, "description": description}


def response_to_html(response):
    content = response.content
    with open('source.html', 'wb') as file:  # using 'wb' to save the content in binary mode
        file.write(content)
        print('Content saved.')


def main() -> None:
    try:
        url = read_url()
        response = get_response(url)
    except InvalidPageException as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
