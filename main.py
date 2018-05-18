from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import json
import os, time, copy

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_driver = os.getcwd() + "/chromedriver"
url_base = "https://nomadlist.com"
cached_countries = []


def start_driver():
    global driver
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)


def end_driver():
    driver.quit()


def get_cities(country_name, amount):
    url_param = "/search/" + country_name
    url = url_base + url_param

    driver.get(url)
    # sleep for 3 seconds so page can redirect to view with search results
    print("Waiting for the page to load: " + url)
    time.sleep(1)

    # grid = driver.find_elements_by_xpath("//*[@class='grid show view']")
    grid = driver.find_element_by_css_selector(".grid.show.view")
    # items = driver.find_elements_by_css_selector(".item.show.show-now")
    items = driver.find_elements_by_xpath("//div[contains(@class, 'item show show-now')]")

    i = 0
    cities = []

    country = {'country': {'name': country_name, 'cities': []}}

    for item in items:
        if i == amount:
            break

        # TODO: first element should be skipped because it's a template thingy, it's class name includes 'template'
        # classes = item.get_attribute("class")
        text = item.find_element_by_css_selector(".text > h3")
        city_element = item.find_element_by_class_name("itemName")
        country_element = item.find_element_by_class_name("itemSub")

        if city_element.text:
            # print("City: " + city.text)
            country['country']['cities'].append(city_element.text)
            # cities.append({'city': city_element.text, 'country': country})
            i = i + 1

        # print("Country: " + country.text)

    cached_countries.append(country)
    return country


def get_cities_from_multiple_countries(countries, amount):
    cities = []
    for country in countries:
        cities.append(get_cities(country, amount))

    return cities


def get_saved_countries(country_names):
    countries = []

    for country_name in country_names:
        for item in cached_countries:
            if item['country']['name'] == country_name:
                countries.append(item)

    return countries


def edit_countries(requested):
    requested_copy = copy.copy(requested)

    for item in requested:
        for country in cached_countries:
            if country['country']['name'] == item:
                requested_copy.remove(item)

    return requested_copy


# print(json.dumps(get_cities('Germany', 10)))
