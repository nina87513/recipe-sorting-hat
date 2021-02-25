import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, url):
        self.url = url

        response = requests.get(url=url)
        self.soup = BeautifulSoup(response.text, 'lxml')

        self.result = ""

    def get_data(self):
        info_items = self.soup.find_all('li', 'ingredients-item')
        for item in info_items:
            self.result += item.find('span',
                                     'ingredients-item-name').text.strip() + '\n'

        paragraph_items = self.soup.find_all('div', 'paragraph')
        for item in paragraph_items:
            self.result += item.find('p').text.strip() + '\n'

        return self.result
