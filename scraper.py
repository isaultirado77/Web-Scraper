import requests


def read_url() -> str:
    url = input('Intput thr URL: \n')
    return url


def get_request(url: str, headers: dict = None):
    return requests.get(url, headers=headers)


def get_joke(request) -> str:
    try:
        data = request.json()
        return data['joke']
    except KeyError:
        print('Invalid resource!')


def main() -> None:
    url = read_url()
    request = get_request(url, {'Accept': 'application/json'})
    if request.status_code == 200:
        joke = get_joke(request)
        print(joke)
    else:
        print('Invalid resource!')


if __name__ == '__main__':
    # print('requests version: ', requests.__version__)
    main()
