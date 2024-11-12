import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3')
