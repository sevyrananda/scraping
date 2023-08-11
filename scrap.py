import requests # import requests untuk mengirim request http ke halaman web
from bs4 import BeautifulSoup # import  BeautifulSoup untuk parsing html
import csv # import csv untuk menyimpan data yang didapat ke file csv

web_url = 'https://www.bukalapak.com/c/aksesoris-rumah-7354/peralatan-makan-minum-7363?page=' # menyimpan link web bukalapak  yang akan discrape ke variabel 
data = []

for page in range(2, 8): # Melakukan perulangan untuk scraping pada halaman 2 hingga 7
    url = web_url + str(page)  # Membuat URL halaman yang akan discrape
    req = requests.get(url)  # Mengirim permintaan HTTP GET ke URL bukalapak
    soup = BeautifulSoup(req.text, 'html.parser')  # Membuat objek BeautifulSoup dari untuk memparse konten HTML
    product_items = soup.find_all('div', {'class': 'bl-product-card'})  # Mencari semua elemen dengan tag div dan class 'bl-product-card' yang disimpan di variabel product_items
    
    for item in product_items: # melakukan perulangan untuk mengambil masing2 item yng telah dicari di variabel product_items
        # Mengambil nama, alamat, harga, dan rating produk dari elemen-elemen yang ditemukan
        name = item.find('a', {'class': 'bl-link'}).text.strip() # Mencari semua elemen dengan tag a dan class 'bl-link' yang disimpan di variabel name
        address = item.find('span', {'class': 'mr-4 bl-product-card__location bl-text bl-text--body-14 bl-text--subdued bl-text--ellipsis__1'}).text.strip() # Mencari semua elemen dengan tag span dan class 'mr-4 bl-product-card__location bl-text bl-text--body-14 bl-text--subdued bl-text--ellipsis__1' yang disimpan di variabel address
        price = item.find('p', {'class': 'bl-text bl-text--subheading-20 bl-text--semi-bold bl-text--ellipsis__1'}).text.strip() # Mencari semua elemen dengan tag p dan class 'bl-text bl-text--subheading-20 bl-text--semi-bold bl-text--ellipsis__1' yang disimpan di variabel price
        rating = item.find('p', {'class': 'bl-text bl-text--body-14 bl-text--subdued'}).text.strip() # Mencari semua elemen dengan tag p dan class 'bl-text bl-text--body-14 bl-text--subdued' yang disimpan di variabel rating
        img_url = item.find('img')['src'] # Mengambil URL gambar
        # Menghindari tautan gambar yang mengarah ke placeholder
        if img_url != 'https://s0.bukalapak.com/ast/bazaar-dweb/base/images/ico_loading.png':
            data.append([name, address, price, rating, img_url]) # Menyimpan data dalam list data

csv_file = 'data_product.csv' # deklarasi nama file CSV untuk menyimpan data

with open(csv_file, 'w', newline='', encoding='utf-8') as file: # Membuka file csv_file dengan mode write ('w') untuk menulis data
    writer = csv.writer(file) # Membuat objek writer dari modul CSV untuk menulis data ke dalam file.
    writer.writerow(['Name', 'Address', 'Price', 'Rating', 'Image_URL']) # Menulis header kolom
    writer.writerows(data) # Menambahkan data ke dalam file CSV
