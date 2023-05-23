
import requests
from bs4 import BeautifulSoup
import csv

url = 'https://ek.ua/ua/list/30/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = soup.find_all('div', class_='model-short-title no-u')
    
    with open('tablets.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(['Модель', 'URL зображення', 'Магазин', 'Ціна'])
        
        for product in products:
            model = product.find('div', class_='model').text.strip()
            image_url = product.find('img')['src']
            store = product.find('div', class_='store').text.strip()
            price = product.find('div', class_='price').text.strip()
            
            writer.writerow([model, image_url, store, price])
            
    print("Дані збережено в файлі tablets.csv")
else:
    print("Помилка при виконанні HTTP-запиту")