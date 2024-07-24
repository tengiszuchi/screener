import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

url_filename_map = {
    "https://companiesmarketcap.com/": "world_market.csv",
    "https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/": "usa_market.csv",
    "https://companiesmarketcap.com/canada/largest-companies-in-canada-by-market-cap/": "canada_market.csv",
    "https://companiesmarketcap.com/mexico/largest-companies-in-mexico-by-market-cap/": "mexico_market.csv",
    "https://companiesmarketcap.com/brazil/largest-companies-in-brazil-by-market-cap/": "brazil_market.csv",
    "https://companiesmarketcap.com/chile/largest-companies-in-chile-by-market-cap/": "chile_market.csv",
    "https://companiesmarketcap.com/european-union/largest-companies-in-the-eu-by-market-cap/": "eu_market.csv",
    "https://companiesmarketcap.com/germany/largest-companies-in-germany-by-market-cap/": "germany_market.csv",
    "https://companiesmarketcap.com/united-kingdom/largest-companies-in-the-uk-by-market-cap/": "uk_market.csv",
    "https://companiesmarketcap.com/france/largest-companies-in-france-by-market-cap/": "france_market.csv",
    "https://companiesmarketcap.com/spain/largest-companies-in-spain-by-market-cap/": "spain_market.csv",
    "https://companiesmarketcap.com/netherlands/largest-companies-in-the-netherlands-by-market-cap/": "netherlands_market.csv",
    "https://companiesmarketcap.com/sweden/largest-companies-in-sweden-by-market-cap/": "sweden_market.csv",
    "https://companiesmarketcap.com/italy/largest-companies-in-italy-by-market-cap/": "italy_market.csv",
    "https://companiesmarketcap.com/switzerland/largest-companies-in-switzerland-by-market-cap/": "switzerland_market.csv",
    "https://companiesmarketcap.com/poland/largest-companies-in-poland-by-market-cap/": "poland_market.csv",
    "https://companiesmarketcap.com/finland/largest-companies-in-finland-by-market-cap/": "finland_market.csv",
    "https://companiesmarketcap.com/china/largest-companies-in-china-by-market-cap/": "china_market.csv",
    "https://companiesmarketcap.com/japan/largest-companies-in-japan-by-market-cap/": "japan_market.csv",
    "https://companiesmarketcap.com/south-korea/largest-companies-in-south-korea-by-market-cap/": "south_korea_market.csv",
    "https://companiesmarketcap.com/hong-kong/largest-companies-in-hong-kong-by-market-cap/": "hong_kong_market.csv",
    "https://companiesmarketcap.com/singapore/largest-companies-in-singapore-by-market-cap/": "singapore_market.csv",
    "https://companiesmarketcap.com/indonesia/largest-companies-in-indonesia-by-market-cap/": "indonesia_market.csv",
    "https://companiesmarketcap.com/india/largest-companies-in-india-by-market-cap/": "india_market.csv",
    "https://companiesmarketcap.com/malaysia/largest-companies-in-malaysia-by-market-cap/": "malaysia_market.csv",
    "https://companiesmarketcap.com/taiwan/largest-companies-in-taiwan-by-market-cap/": "taiwan_market.csv",
    "https://companiesmarketcap.com/thailand/largest-companies-in-thailand-by-market-cap/": "thailand_market.csv",
    "https://companiesmarketcap.com/australia/largest-companies-in-australia-by-market-cap/": "australia_market.csv",
    "https://companiesmarketcap.com/new-zealand/largest-companies-in-new-zealand-by-market-cap/": "new_zealand_market.csv",
    "https://companiesmarketcap.com/israel/largest-companies-in-israel-by-market-cap/": "israel_market.csv",
    "https://companiesmarketcap.com/saudi-arabia/largest-companies-in-saudi-arabia-by-market-cap/": "saudi_arabia_market.csv",
    "https://companiesmarketcap.com/turkey/largest-companies-in-turkey-by-market-cap/": "turkey_market.csv",
    "https://companiesmarketcap.com/russia/largest-companies-in-russia-by-market-cap/": "russia_market.csv",
    "https://companiesmarketcap.com/south-africa/largest-companies-in-south-africa-by-market-cap/": "south_africa_market.csv",
}

flag_to_country_code = {
    "🇺🇸": "US",
    "🇨🇳": "CN",
    "🇨🇦": "CA",
    "🇲🇽": "MX",
    "🇧🇷": "BR",
    "🇨🇱": "CL",
    "🇪🇺": "EU",
    "🇩🇪": "DE",
    "🇬🇧": "GB",
    "🇫🇷": "FR",
    "🇪🇸": "ES",
    "🇳🇱": "NL",
    "🇸🇪": "SE",
    "🇮🇹": "IT",
    "🇨🇭": "CH",
    "🇵🇱": "PL",
    "🇫🇮": "FI",
    "🇯🇵": "JP",
    "🇰🇷": "KR",
    "🇭🇰": "HK",
    "🇸🇬": "SG",
    "🇮🇩": "ID",
    "🇮🇳": "IN",
    "🇲🇾": "MY",
    "🇹🇼": "TW",
    "🇹🇭": "TH",
    "🇦🇺": "AU",
    "🇳🇿": "NZ",
    "🇮🇱": "IL",
    "🇸🇦": "SA",
    "🇹🇷": "TR",
    "🇷🇺": "RU",
    "🇿🇦": "ZA",
    "🇮🇪": "IE",
    "🇩🇰": "DK",
    "🇧🇪": "BE",
    "🇦🇹": "AT"
}

virgin_messages = [
    "virgin API consoomer fears HTML",
    "virgin API consoomer limited to what the API can do",
    "virgin API consoomer has to identify himself even for read-only APIs",
    "virgin API consoomer API provider takes away his endpoint",
    "virgin API consoomer 429 too many requests",
    "virgin API consoomer has to worry about quota",
    "virgin API consoomer thinks that he is making his life easier",
    "virgin API consoomer begs his users for Oauth",
    "virgin API consoomer API keys (lol)",
    "virgin API consoomer data is 10 minutes behind anyways",
    "virgin API consoomer has to verify his email, phone, driver's license, SSN, DNA sample",
    "virgin API consoomer has to agree to ToS and follow the rules (LMAO)"
]

chad_messages = [
    "Chad 3rd party scraper follows no rules, doesn’t agree to any terms and service",
    "Chad 3rd party scraper scrapes so fast the backend crashes",
    "Chad 3rd party scraper has no limitations and can access any data he wants",
    "Chad 3rd party scraper entire industries are dedicated to stopping him",
    "Chad 3rd party scraper website thinks his user agent is a phone",
    "Chad 3rd party scraper promising career at high-frequency trading firm (just scrapes in spare time)",
    "Chad 3rd party scraper pays Indians to solve captchas",
    "Chad 3rd party scraper can work anonymously",
    "Chad 3rd party scraper curl://",
    "Chad 3rd party scraper Selenium goat",
    "Chad 3rd party scraper millions of engineer hours can’t stop him from scraping"
]

def print_random_message():
    if random.choice([True, False]):
        print(random.choice(virgin_messages))
    else:
        print(random.choice(chad_messages))

def get_country_code(flag_emoji):
    return flag_to_country_code.get(flag_emoji, 'Unknown')

os.makedirs("output", exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless")

service = Service(ChromeDriverManager().install())

while True:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    total_start_time = time.time()
    
    urls_scraped = 0
    csvs_created = 0
    
    for url, filename in url_filename_map.items():
        print(f"Opening {url}")
        start_time = time.time()
        driver.get(url)
        driver.implicitly_wait(10)
        print(f"Started scraping {url}")
    
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    
        table = soup.find('table', {'class': 'default-table table marketcap-table dataTable'})
    
        data = []
        for row in table.tbody.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) >= 5:
                rank = columns[1].text.strip()
                name = columns[2].find('div', {'class': 'company-name'}).text.strip()
                market_cap = columns[3].text.strip()
                price = columns[4].text.strip()
                country_flag = columns[7].text.strip().split()[0]
                country_code = get_country_code(country_flag)
                data.append([rank, name, market_cap, price, country_code])
                print(f"Finished scraping {name} at {market_cap} total market cap at {price} price per share")
    
        df = pd.DataFrame(data, columns=['Rank', 'Name', 'Market Cap', 'Price', 'Country'])
    
        output_path = os.path.join("output", filename)
        df.to_csv(output_path, index=False)
        print(f"Finished scraping {url} and saved to {output_path}")
    
        urls_scraped += 1
        csvs_created += 1
    
        end_time = time.time()
        print(f"Time taken for {url}: {end_time - start_time:.2f} seconds")
    
    driver.quit()
    
    total_end_time = time.time()
    total_time_taken = total_end_time - total_start_time
    
    print(f"Total URLs scraped: {urls_scraped}")
    print(f"Total CSVs created: {csvs_created}")
    print(f"Total time taken: {total_time_taken:.2f} seconds")
    
    print("Sleeping for 60 seconds before the next run...")
    for _ in range(60):
        print_random_message()
        time.sleep(1)
