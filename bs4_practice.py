import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.newsinlevels.com/products/albino-tortoise-level-1/')

# Create a parse tree
# r.content: data of the page
# 'html.parser' python built-in parser
soup = BeautifulSoup(r.content, 'html.parser')


def main():
    print('Status Request', r.status_code, end='\n')
    # print(soup.prettify())  # Give a format to the tree
    # print(soup.find('title'))
    # print(soup.head)
    paragraphs = soup.find_all('p', {'style': 'text-align: center;'})
    for p in paragraphs:
        print(p.text + '\n')


if __name__ == '__main__':
    main()
