import requests
from bs4 import BeautifulSoup

city_ids = {
    'sofia': '100727011',
    'plovdiv': '100728193',
    'varna': '100726050',
    'burgas': '100732770',
    'ruse': '100727523',
    'stara-zagora': '100726848',
    'pleven': '100728203',
    'dobrich': '100726418',
    'shumen': '100727233',
    'montana': '100729114',
}

BASE_URL = 'https://www.sinoptik.bg/'
city = input('Choose city: ').lower()
url = BASE_URL + city + '-bulgaria-' + city_ids[city]
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

curr_temp_title, curr_temp_value = (
    'Температура:',
    soup.find('span', {'class': 'wfCurrentTemp'}).string,
)
details = soup.find_all('span', class_='wfNonCurrentValue')[::-1]

data = {
    curr_temp_title: curr_temp_value,
}

for wrapper in soup.find_all('div', class_='wfCurrentWrapper'):
    heading = wrapper.find('span', class_='wfCurrentHeading').text.strip()
    value = wrapper.find('span', class_='wfCurrentValue').text.strip()
    data[heading] = value
    if not data[heading]:
        data[heading] = details[-1].get_text(separator=' ', strip=True)
        details.pop()

for heading, value in data.items():
    if value:
        print(f'{heading} {value}')
