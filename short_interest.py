import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.text import Text
from rich.panel import Panel

YAHOO_FINANCE_URL = "https://finance.yahoo.com/quote/{}/key-statistics"

def fetch_short_interest_data(symbol):
    """Fetches short interest data for a given stock symbol from Yahoo Finance."""
    try:
        url = YAHOO_FINANCE_URL.format(symbol)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract short interest-related stats (example extraction)
        stats = {}
        stats["Symbol"] = symbol.upper()
        stats["Short Interest"] = "N/A"
        stats["Days to Cover"] = "N/A"
        stats["Float"] = "N/A"
        
        # Searching for the statistics table that contains relevant data
        tables = soup.find_all('table')
        for table in tables:
            if "Short Percent of Float" in table.text:
                rows = table.find_all('tr')
                for row in rows:
                    if "Short Percent of Float" in row.text:
                        stats["Short Interest"] = row.find_all('td')[1].text.strip()
                    if "Shares Short (prior month)" in row.text:
                        stats["Days to Cover"] = row.find_all('td')[1].text.strip()
                    if "Float" in row.text:
                        stats["Float"] = row.find_all('td')[1].text.strip()
        
        return stats
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def display_short_interest_table(short_interest_data):
    """Displays short interest data in a nicely formatted table."""
    console = Console()
    
    # Define the start and end colors for the gradient
    start_color = (30, 144, 255)  # Light blue
    end_color = (255, 69, 0)      # Red
    
    # Generate gradient for table title
    gradient_colors = generate_gradient_color(start_color, end_color, len("Short Interest Screener"))
    title_text = Text()
    for idx, char in enumerate("Short Interest Screener"):
        color = gradient_colors[idx]
        title_text.append(char, style=Style(color=color, bold=True))
    
    console.print(Panel(title_text, expand=False, border_style="bold white"))
    
    # Create a table for displaying the short interest data
    header_style = Style(color="white", bold=True)
    table = Table(show_header=True, header_style=header_style)
    
    table.add_column("Symbol", justify="center")
    table.add_column("Short Interest (%)", justify="right")
    table.add_column("Days to Cover", justify="right")
    table.add_column("Float", justify="right")
    
    if short_interest_data:
        table.add_row(
            short_interest_data["Symbol"],
            short_interest_data["Short Interest"],
            short_interest_data["Days to Cover"],
            short_interest_data["Float"]
        )
    
    console.print(table)

def generate_gradient_color(start_rgb, end_rgb, steps):
    """Generates a list of RGB color strings creating a gradient from start_rgb to end_rgb."""
    gradient_colors = []
    for step in range(steps):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (step / (steps - 1)))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (step / (steps - 1)))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (step / (steps - 1)))
        gradient_colors.append(f"rgb({r},{g},{b})")
    return gradient_colors

def main():
    # Example symbols
    symbols = ["AAPL", "TSLA", "GME"]  # Replace with any stock symbol of interest
    
    # Fetch and display data for each symbol
    for symbol in symbols:
        short_interest_data = fetch_short_interest_data(symbol)
        if short_interest_data:
            display_short_interest_table(short_interest_data)
        else:
            print(f"Failed to fetch data for {symbol}.")

if __name__ == "__main__":
    main()
