import requests
from bs4 import BeautifulSoup as BS
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_soup(html):
    soup = BS(html,'lxml')
    return soup

def get_data(soup):
    catalog = soup.find('div', class_='search-results-table')
    cars = catalog.find_all('div', class_='list-item list-label')
    for car in cars:
        try:
            title = car.find('h2', class_='name').text.strip()
        except AttributeError:
            title = 'нет наименования'
        try:
            price = car.find('div', class_= 'block price').find('div').text
        except AttributeError:
            price = 'цена не указана'
        try:
            image = car.find('img', class_='lazy-image').get('data-src')
        except AttributeError:
            image = 'нет фото'
        try:
            description_= car.find('div', class_='block info-wrapper item-info-wrapper').text.split()
            description2 = ','.join(description_)
            description = description2.replace(',,',',')
        except AttributeError:
            description = 'нет информации'
        # print(car)
        
        write_csv({
            'title':title,
            'price': price,
            'image':image,
            'description': description
        })
    

def write_csv(data):
    with open('cars.csv', 'a') as file:
        names = ['title', 'price', 'image', 'description']
        write = csv.DictWriter(file,delimiter= ',', fieldnames=names)
        write.writerow(data)

def main():
    for i in range(1,1049):
        try:
            BASE_URL =f'https://www.mashina.kg/search/all/?page={i}'
            html = get_html(BASE_URL)
            soup = get_soup(html)
            get_data(soup)
            print(f'спарсили{i} страницу')
        except:
            print('Конец. Это последняя страница')

if __name__=='__main__':
    main()