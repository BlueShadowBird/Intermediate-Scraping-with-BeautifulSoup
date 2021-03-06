import requests
from bs4 import BeautifulSoup

session = requests.session()


def scrap():
    scrap_result = []
    url = 'http://127.0.0.1:5000/login'
    data = {
        'username': 'user',
        'password': 'user12345'
    }
    response_text = session.post(url, data).text
    soup = BeautifulSoup(response_text, 'html.parser')
    items = soup.find_all('div', attrs={'class': 'card h-100'})
    for item in items:
        scrap_result.append(parse_detail(item))

    page_number = len(soup.find('ul', attrs={'class': 'pagination'}).find_all('li', attrs={'class': 'page-item'}))-2

    for page in range(2, page_number + 1):
        response = session.get(f'http://127.0.0.1:5000/?page={page}')
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', attrs={'class': 'card h-100'})
        for item in items:
            scrap_result.append(parse_detail(item))
    return scrap_result


def parse_detail(item):
    result_detail = {}
    url = item.find('h4').find('a')['href']
    res = session.get(f'http://127.0.0.1:5000{url}')
    soup = BeautifulSoup(res.text, 'html.parser')
    result_detail['image'] = soup.find('div', attrs={'class': 'card mt-4'}).find('img')
    div = soup.find('div', attrs={'class': 'card-body'})
    result_detail['title'] = div.find('h3', attrs={'class': 'card-title'}).text
    result_detail['price'] = div.find('h4', attrs={'class': 'card-price'}).text
    result_detail['stock'] = div.find('span', attrs={'class': 'card-stock'}).text.replace('stock: ', '')
    result_detail['category'] = div.find('span', attrs={'class': 'card-category'}).text.replace('category: ', '')
    result_detail['description'] = div.find('p', attrs={'class': 'card-text'}).text.replace('Description: ', '')

    return result_detail
