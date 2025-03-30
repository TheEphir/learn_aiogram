import requests
import pkg.sale_urls
from bs4 import BeautifulSoup

def check_sale_rztk(price_info: BeautifulSoup) -> bool:
    sale = price_info.find("p", class_="product-price__small")
    return bool(sale)

def get_item_info_rztk(url) -> dict:
    """
    Scrape price info and image url of goods from https://rozetka.com.ua/ua/
    """
    site = requests.get(url).text
    soup = BeautifulSoup(site, features="html.parser")
    
    image_url = soup.find("app-slider", class_="main-slider").find("img")["src"]
    
    price_info = soup.find("div", class_="product-price__wrap")
    if check_sale_rztk(price_info):
        price = price_info.find("p", class_="product-price__small").text
        sale_price = price_info.find("p",class_="product-price__big").text
        return  {
            "url": url,
            "price": f"Sale!\n{price} -> {sale_price}",
            "image_url": image_url
        }
    else:
        price = price_info.find("p",class_="product-price__big").text
        return  {
            "url": url,
            "price": f"Not on sale!\n{price}",
            "image_url": image_url
        }


def add_item(item_info: dict) -> None:
    """
    add new item to urls file
    """
    items = pkg.sale_urls.read_url_file()
    items.update(item_info)
    pkg.sale_urls.write_to_url_file(items)


def remove_item(item_name:str) -> None:
    """
    complementary to add_item()
    """
    items = pkg.sale_urls.read_url_file()
    items.pop(item_name)
    pkg.sale_urls.write_to_url_file(items)
    