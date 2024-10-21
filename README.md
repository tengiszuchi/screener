# Screener

The **Screener** project scrapes market data from various countries' stock market pages on the [companiesmarketcap.com](https://companiesmarketcap.com/) website. It extracts information such as the rank, company name, market cap, price, and country, and saves the data into CSV files for further analysis. Additionally, the project provides a script to launch the scraper in a new terminal window.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Files Description](#files-description)
- [Notes](#notes)

## Installation

Before using this project, ensure you have the following prerequisites installed:

1. **Python 3.x** - You can download it [here](https://www.python.org/downloads/).
2. **Google Chrome** - The scraper uses Chrome for web scraping.
3. **Chrome WebDriver** - Installable via `webdriver_manager`.

### Step-by-Step Guide:

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd screener
   ```

2. **Install Required Packages:**
   Use `pip` to install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure ChromeDriver Compatibility:**
   Make sure the version of ChromeDriver matches your Chrome browser version. `webdriver_manager` should handle this automatically.

## Usage

### Running the Screener:

The **Screener** script (`screener.py`) scrapes data from various pages and saves it to CSV files in the `output` directory. You can run it using:

```bash
python screener.py
```

### Launching the Scraper in a New Terminal Window:

To run the scraper in a new Terminal window on macOS, use the `launch_screener.py` script:

```bash
python launch_screener.py
```

This script will open a new terminal and start the scraping process automatically.

## Examples

### Example 1: Running `screener.py` Directly

1. Navigate to the project directory:
   ```bash
   cd screener
   ```
2. Run the scraper:
   ```bash
   python screener.py
   ```
3. The scraper will start, open Chrome, and begin collecting data from multiple URLs. Once done, the data will be saved in `output` as individual CSV files, such as `usa_market.csv`, `china_market.csv`, etc.

### Example 2: Using `launch_screener.py` to Open a New Terminal

1. Make sure you are in the project directory.
2. Run the following command:
   ```bash
   python launch_screener.py
   ```
3. A new Terminal window will open, and the scraper will start running in that window. This is helpful if you want to keep the scraping process separate from other tasks.

### Example 3: Running the CSV Viewer

After scraping data, you can view the collected data using the `main.py` script, which will prompt you to select a CSV file from the `output` directory:

```bash
python main.py
```

1. Select the file you want to analyze by entering its corresponding number.
2. The data will be displayed in a formatted table, and additional options like charts and random company focus will be shown.

## Files Description

- **`screener.py`**: The main scraper script. It scrapes data from predefined URLs and saves it as CSV files.
- **`main.py`**: A script that allows you to interactively view the data collected in the CSV files, displaying formatted tables and visualizations.
- **`launch_screener.py`**: A script to launch the scraper in a new Terminal window on macOS.
- **`requirements.txt`**: Lists all required packages to run the project.
- **`output/`**: This directory is where the scraped CSV files are saved.

## Notes

1. **ChromeDriver Management**: The scraper uses `webdriver_manager` to handle ChromeDriver installation. It should automatically fetch the right version based on your installed Chrome browser.
2. **Headless Mode**: The scraper runs in headless mode by default, which means Chrome will not visibly open. If you want to see Chrome in action, remove or comment out the line:
   ```python
   chrome_options.add_argument("--headless")
   ```

3. **Dynamic Content**: Some sites may change their HTML structure, which might cause the scraper to break. If this happens, you might need to update the selector in the `screener.py` script.
