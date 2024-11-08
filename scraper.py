import requests


def read_url() -> str:
    url = input('Intput thr URL: \n')
    return url


def get_request(url: str, headers: dict = None):
    return requests.get(url, headers=headers)


def main() -> None:
    url = 'https://icanhazdadjoke.com/j/LBAQ79MJmb'
    request = get_request(url, {'Accept': 'application/json'})
    if request.status_code == 200:
        data = request.json()
        print(data['joke'])
    else:
        print('Invalid resource!')


if __name__ == '__main__':
    # print('requests version: ', requests.__version__)
    main()
