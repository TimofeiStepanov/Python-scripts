import requests
import bs4
import os
import re
import unicodedata
import time
import pandas
import argparse
import openpyxl
import xlsxwriter
import xlrd



t = time.time()

BASE_URL = "https://babybug.ru"
URL = "https://babybug.ru/brendy/melissa/"

def args():
     parser = argparse.ArgumentParser()
     parser.add_argument("-f",help="Input absolute path to folder for parsed images save."
                                                       "Example: D:\Workdir\Images")

     return parser.parse_args()

def open_page():
    page = requests.get(URL)
    page_text = page.text
    return page_text


def card_product():
    """ """
    soup = bs4.BeautifulSoup(open_page(), 'html.parser')
    product = soup.div("div", class_="product-card group")
    return product


def name_product():
    names_products_sp = []
    for card in cards:
        name_tag = card("a", class_="product-card__title")
        for name_prod in name_tag:
            for name_product in name_prod.stripped_strings:
                name_of_product: str = repr(name_product)
                names_products_sp.append(name_of_product)
    return names_products_sp


def link_product():
    links_to_products_sp = []
    for card in cards:
        name_tag = card("a", class_="product-card__title")
        for name_prod in name_tag:
            link = name_prod.get('href')
            link_to_product = str(BASE_URL + link)
            links_to_products_sp.append(link_to_product)
    return links_to_products_sp


def img_product():
    img_of_product_links_sp = []
    link_to_img_sp = []
    for card in cards:
        images_tag = card("img", class_="product-card__img")
        for img in images_tag:
            image_link = img.get("src")
            link_to_img: str = str(BASE_URL + image_link)
            link_to_img_sp.append(link_to_img)
        tmp = link_to_img_sp.copy()
        img_of_product_links_sp.append(tmp)
        link_to_img_sp.clear()
    return img_of_product_links_sp


def price_product():
    price_of_product_sp = []
    for card in cards:
        price_tag = card("div", class_=re.compile("product-card__prices"))
        for pr in price_tag:
            price = pr.span
            price_p = price.text
            price_of_product = unicodedata.normalize("NFKD", price_p)
            price_of_product_sp.append(price_of_product)
    return price_of_product_sp

if __name__ == '__main__':
    cards = card_product()
    names = name_product()
    links = link_product()
    images = img_product()
    prices = price_product()
    picture_folders = []
    folder = args()


    if not os.path.exists(folder.f):
        os.mkdir(folder.f)
    i = 0
    for img in images:
        name = names[i]
        picture_folder = folder.f + "\\" + name
        #picture_folder = ""
        if not os.path.exists(folder.f + "\\" + name):
            os.mkdir(picture_folder)
        picture_folders.append(picture_folder)
        i = i + 1

        count = 1
        for image in img:
            picture = requests.get(image)
            with open(picture_folder+"\\"+str(count)+".jpg", "wb") as file:
                file.write(picture.content)
            count = count + 1

    data_result = pandas.DataFrame(
        {'Product': names,
         'Price': prices,
         'Link': links,
         'Picture': picture_folders}
    )
    result_excel_file = pandas.ExcelWriter(folder.f + "\\" + 'pars_res.xlsx', engine='xlsxwriter')
    data_result.to_excel(result_excel_file)
    result_excel_file.save()

print(f"time {time.time() - t}")
