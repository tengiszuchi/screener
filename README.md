# Market Cap Scraper

This script scrapes the largest companies by market capitalization from various countries and regions listed on the website [companiesmarketcap.com](https://companiesmarketcap.com/) and saves the data to CSV files. The script is designed to run continuously, scraping data every minute.

## Features

- Scrapes company rankings, names, market capitalizations, share prices, and country information.
- Saves the scraped data to CSV files in the `output` directory.
- Prints progress updates and timing information to the terminal.

## Installation Requirements

1. **Python**: Make sure you have Python 3.x installed on your system.

2. **Install required Python packages**:
    ```bash
    pip install selenium beautifulsoup4 pandas webdriver-manager
    ```

3. **Google Chrome**: The script uses Google Chrome for web scraping. Ensure you have Google Chrome installed.

## Usage

1. **Save the script**: Save the provided script as `main.py`.

2. **Run the script**:
    ```bash
    python main.py
    ```

   The script will start running in an infinite loop, scraping data every minute and printing updates to the terminal.

## Script Details

### URL to Filename Mapping

The `url_filename_map` dictionary contains mappings from the URLs of the pages to be scraped to the filenames of the CSV files where the data will be saved.

### Country Code Mapping

The `flag_to_country_code` dictionary maps country flag emojis to their corresponding country codes.

### Scraping and Saving Data

The script uses Selenium to open each URL and BeautifulSoup to parse the HTML content. It extracts the required data from the table on the page, creates a DataFrame using Pandas, and saves it to a CSV file in the `output` directory.

### Continuous Running

The script runs in an infinite loop, with a 60-second sleep interval between each iteration, ensuring that the data is scraped continuously every minute.
