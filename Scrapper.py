from bs4 import BeautifulSoup

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from selenium import webdriver

import pandas as pd

import plotly.express as px


def scrape(link):

    exe_path = 'C:/Users/aspen/OneDrive/Desktop/Sp2023 Classes/Python Programming/Project 2/geckodriver32.exe'

    service = Service(executable_path=exe_path)

    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

    driver = webdriver.Firefox(service=service, options=options)
    driver.get(link)
    response = driver.page_source

    soup = BeautifulSoup(response, "html.parser")

    listings = soup.find_all(
        "div", class_="relative flex h-full w-full flex-col overflow-hidden rounded border border-gray-200 xl:h-[443px]")

    apartments = {}

    for listing in listings:
        price = listing.find(
            "p", class_="flex flex-1 items-center text-lg font-semibold text-black").get_text()

        apartment = listing.find(
            "p", class_="block font-semibold text-black overflow-hidden overflow-ellipsis whitespace-nowrap").get_text()

        address = listing.find(
            "p", class_="overflow-hidden overflow-ellipsis whitespace-nowrap font-normal text-body-color").get_text()

        bed_bath = listing.find(
            "p", attrs={"data-tid": "beds-baths"}).get_text()

        phone = listing.find("a", class_="h-40 inline-flex justify-center items-center font-semibold rounded outline-none cursor-pointer hover:no-underline disabled:cursor-not-allowed primary-cta hover-bg-light hover-transition basis-1/2 shrink grow-0 z-10 xs:before:icon-phone xs:before:pr-6 xs:before:text-body xs:before:font-normal xs:before:leading-none").get_text()

        try:
            reviews = listing.find_all(
                "span", class_="sr-only")[2].get_text()
        except:
            reviews = "No Reviews"

        apartments[apartment] = {"Price": price, "Address": address,
                                 "Beds and Baths": bed_bath, "Phone Number": phone, "Reviews": reviews}

    df = pd.DataFrame(apartments)

    df = df.T

    df.sort_values(by=['Price'], ascending=True)

    df.to_csv("Output.csv")

    # figure = px.bar(df, layout_title_text="Sales Prices of Apartments", y="Price")

    figure = px.scatter(df, y="Beds and Baths", x="Price")

    figure.show()


# (Rent.com)
# ---------------------------
# Line 870
# Line 4180
# flex-1 px-16 text-inherit no-underline hover:no-underline classes for listing info (tailwind) (Find another way to ID Listings)
scrape("https://www.rent.com/new-jersey/union-apartments")
