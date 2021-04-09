from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from time import sleep
from math import ceil
from sys import argv
from random import randint
import config
import shutil
import os
import subprocess


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}


def main():
    global browser
    url = "https://kaspi.kz/merchantcabinet/#/offers"
    browser.get(url)
    sleep(5.2)

    print("Парсинг страниц...")
    products = []
    for j in range(int(int(str(browser.find_element_by_css_selector(".gwt-HTML").text).split(" ")[-1]) // 10)+1):
        resp = browser.find_elements_by_css_selector(".GPGV22TBBR > tbody:nth-child(3)")
        for i in resp[0].find_elements_by_tag_name("tr"):
            if len(i.find_elements_by_class_name("offer-managment__pending-icon")) > 0:
                continue
            products.append({
                "id":   i.find_elements_by_class_name("offer-managment__product-cell-meta-text")[1].text,
                "url":  i.find_element_by_class_name("offer-managment__product-cell-link").get_attribute("href"),
                #"price": int(str(i.find_element_by_class_name("offer-managment__price-cell-price").text).replace(" ", "")),
            })
        browser.find_element_by_css_selector("td.GPGV22TBJH:nth-child(4) > img:nth-child(1)").click()
        sleep(3)
    print(len(products))
    print("------------------------------------")

    editProducts = []
    for product in products:
        print(f"Проверка {product['id']}...")
        print(product["url"])
        browser.get(product["url"])

        sleep(2.3)
        line = browser.find_element_by_css_selector(".sellers-table__self > tbody:nth-child(3) > tr:nth-child(1)")

        if "GLAMOUR BABY" == str(line.find_element_by_css_selector("td:nth-child(1) > a:nth-child(1)").text):
            continue

        newprice = int(str(line.find_element_by_css_selector("td:nth-child(4) > div:nth-child(1)").text)[:-1].replace(" ", "")) - 10
        #print(f"{product['id']} - проверка")
        if product["id"] in config.minPrice.keys() and config.minPrice[product["id"]] <= newprice:
            editProducts.append({
                "id":       product["id"],
                "newprice": newprice
            })
        elif not product["id"] in config.minPrice.keys():
            editProducts.append({
                "id":       product["id"],
                "newprice": newprice
            })

    print(len(editProducts))
    print("--------------")

    for product in editProducts:
        url = f"https://kaspi.kz/merchantcabinet/#/offers/edit/{product['id']}"
        browser.get(url)
        sleep(4)
        browser.find_element_by_css_selector(".g-mb_tiny > label:nth-child(2)").click()
        browser.find_element_by_css_selector("input.form__col").send_keys(product["newprice"])
        browser.find_element_by_css_selector("button.button:nth-child(1)").click()
        print(f'{product["id"]} - цена понижена!')
        #exit()
    #browser.close()

def start(timer=True):
    global browser
    print("Авторизация...")
    url = "https://kaspi.kz/merchantcabinet/login"
    try:
        browser.get(url)
        sleep(1)
        browser.find_element_by_css_selector('#email').send_keys("") # TODO
        browser.find_element_by_css_selector('#password').send_keys("") # TODO
        browser.find_element_by_css_selector('.button').click()
        sleep(1)
    except: pass
    #main()
    #exit()
    try:
        main()
    except:
        print("ERROR")
        start(False)
    if timer:
        print("FINAL!")
        sleep(randint(10, 15) * 60)
    else:
        return

if __name__ == '__main__':
    global browser
    opts = Options()
    opts.set_headless()
    assert opts.headless
    #print(binary)
    #global browser
    if len(argv) > 1 and argv[1] != "0":
        binary = argv[1]
        browser = Firefox(options=opts, firefox_binary=binary)
    else:
        browser = Firefox(options=opts)
    if len(argv) > 1:
        tempdir = argv[2]
    else:
        tempdir = False

    while True:
        if tempdir:
            del_dir = tempdir
            pObj = subprocess.Popen('del /S /Q /F %s\\*.*' % del_dir, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            rTup = pObj.communicate()
            rCod = pObj.returncode
            if rCod == 0:
                print('Успех: Очищенная Временная папка Windows')
            else:
                print('Сбой: Не удается очистить временную папку Windows')
        start()