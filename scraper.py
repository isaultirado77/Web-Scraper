import requests
from bs4 import BeautifulSoup


class InvalidPageException(Exception):
    def __init__(self, msg):
        super.__init__(msg)


def read_url() -> str:
    url = input('Intput thr URL: \n')
    if 'nature' not in url and 'articles' not in url:
        raise InvalidPageException('Invalid page!')
    return url


def get_response(url: str, headers: dict = None):
    return requests.get(url, headers=headers)


def main() -> None:
    try:
        url = read_url()
        response = get_response(url)
        soup = BeautifulSoup(response.content, 'html.parser')
    except InvalidPageException as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
