from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd

list_urls = [
    #Gaming Links 
    "https://www.emag.bg/laptopi/filter/kapacitet-pamet-f7886,12-16-gb-v25916/kapacitet-pamet-f7886,nad-16-gb-v25917/tip-video-pamet-f7895,dopylnitelna-v-2754/tip-syhranenie-f7941,ssd-v-4670679/price,between-1000-and-3000/rating,star-4/c?ref=lst_leftbar_6420_4-5",
    #Everyday/Home 
    "https://www.emag.bg/laptopi/filter/kapacitet-pamet-f7886,6-8-gb-v25915/tip-video-pamet-f7895,vgradena-v-2755/price,between-500-and-1000/rating,star-4/c?ref=lst_leftbar_6420_4-5",
    #Office 
    "https://www.emag.bg/laptopi/filter/kapacitet-pamet-f7886,12-16-gb-v25916/tip-video-pamet-f7895,vgradena-v-2755/avtonomija-baterija-f7901,nad-6-h-v25862/tip-syhranenie-f7941,ssd-v-4670679/kapacitet-ssd-f9203,500-gb-v-4694038/kapacitet-ssd-f9203,1-tb-v-4690219/kapacitet-ssd-f9203,512-gb-v-4685751/price,between-979-and-5732/rating,star-4/c"
]

def get_html_list():
    htmls = []
    with sync_playwright() as pl:
        browser = pl.firefox.launch(headless=False)
        page = browser.new_page()
        for url in list_urls:
            page.goto(url)
            page.wait_for_selector("div#card_grid")
            htmls.append(page.inner_html("div#card_grid"))
    return htmls

def scraping_html_info(htmls):
    category_list = []
    for html in htmls:
        soup_main_scraper = bs(html, "html.parser")
        card_selector_scraper = soup_main_scraper.select("div.card-v2-wrapper")
        products = []
        for card in card_selector_scraper:
            title = card.select_one("div.pad-hrz-xs h2.card-v2-title-wrapper a").text.strip()
            price = card.select_one("div.card-v2-content div.card-v2-pricing p.product-new-price").text.strip()
            link_product = card.select_one("div.card-v2-info a").attrs["href"]
            image_product = card.select_one("div.card-v2-info div.card-v2-thumb-inner img.w-100").attrs['src']
            unavaibility = card.select_one("div.card-v2-wrapper div.card-v2-info div.pad-hrz-xs div.card-estimate-placeholder div.text-availability-unavailable")
            out_of_stock = card.select_one("div.card-v2-wrapper div.card-v2-info div.pad-hrz-xs div.card-estimate-placeholder div.text-availability-out_of_stock")
            product_attributes  = (title, price, link_product, image_product, unavaibility, out_of_stock)
            products.append(product_attributes)
        category_list.append(products)
    return category_list

def csv_export(category_list):
    with open("mainList.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for product in category_list:
            writer.writerow([product])

