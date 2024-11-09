import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.nature.com/articles/d41586-022-04498-3')

# Create a parse tree
# r.content: data of the page
# 'html.parser' python built-in parser
soup = BeautifulSoup(r.content, 'html.parser')


def main():
    print('Status Request', r.status_code, end='\n')
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    print(title)
    description_tag = soup.find('meta', {'name': 'description'})
    description = description_tag['content'].strip() if description_tag else "No description found"
    print(description)
