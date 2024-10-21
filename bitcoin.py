import requests
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.text import Text
from rich.panel import Panel

# Endpoint for getting prices of multiple cryptocurrencies from CoinGecko API
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",  # Get prices in USD
    "order": "market_cap_desc",  # Order by market cap descending
    "per_page": 50,  # Adjust this number to get more cryptocurrencies
    "page": 1,
    "sparkline": False
}

def fetch_crypto_data():
    """Fetches cryptocurrency data from the CoinGecko API and returns it as a list."""
    try:
        response = requests.get(API_URL, params=PARAMS)
        if response.status_code == 200:
            crypto_data = response.json()
            crypto_prices = []
            
            # Extracting data for each cryptocurrency
            for crypto in crypto_data:
                name = crypto.get("name", "N/A")
                symbol = crypto.get("symbol", "N/A").upper()
                price = crypto.get("current_price", 0.0)
                market_cap = crypto.get("market_cap", 0.0)
                
                # Creating a list for each entry
                crypto_prices.append([name, symbol, price, market_cap])
                
            return crypto_prices
        else:
            print("Failed to fetch data. Please check the API.")
            return []
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def generate_gradient_color(start_rgb, end_rgb, steps):
    """Generates a list of RGB color strings creating a gradient from start_rgb to end_rgb."""
    gradient_colors = []
    for step in range(steps):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (step / (steps - 1)))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (step / (steps - 1)))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (step / (steps - 1)))
        gradient_colors.append(f"rgb({r},{g},{b})")
    return gradient_colors

def display_terminal_title(console, start_color, end_color):
    # Create a gradient for the title text
    gradient_colors = generate_gradient_color(start_color, end_color, len("Crypto Screener"))
    title_text = Text()

    # Apply gradient to each letter
    for idx, char in enumerate("Crypto Screener"):
        color = gradient_colors[idx]
        title_text.append(char, style=Style(color=color, bold=True))
    
    # Create a larger title using a Panel for emphasis
    console.print(Panel(title_text, expand=False, border_style="bold white"))

def display_crypto_table(crypto_data):
    """Displays cryptocurrency data in a nicely formatted table."""
    console = Console()
    
    # Define the start and end colors for the gradient
    start_color = (30, 144, 255)  # Light blue
    end_color = (255, 69, 0)      # Red
    
    # Show terminal title with gradient
    display_terminal_title(console, start_color, end_color)
    
    # Generate a gradient list based on the number of rows to display
    gradient_colors = generate_gradient_color(start_color, end_color, 50)
    
    # Define table with a bold header style
    header_style = Style(color="white", bold=True)
    table = Table(show_header=True, header_style=header_style)
    
    table.add_column("Name", justify="left")
    table.add_column("Symbol", justify="center")
    table.add_column("Price (USD)", justify="right")
    table.add_column("Market Cap (USD)", justify="right")
    
    # Populate the table with data, applying gradient colors to rows
    for idx, entry in enumerate(crypto_data):
        row_style = Style(color=gradient_colors[idx % len(gradient_colors)], bold=True)
        table.add_row(
            entry[0],
            entry[1],
            f"${entry[2]:,.2f}",
            f"${entry[3]:,.0f}",
            style=row_style
        )
    
    # Display the table
    console.print(table)

def main():
    # Fetch data from the API
    crypto_data = fetch_crypto_data()
    
    if crypto_data:
        # Display the fetched data in a table
        display_crypto_table(crypto_data)
    else:
        print("No data found.")

if __name__ == "__main__":
    main()
