import requests
import termplotlib as tpl
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.panel import Panel
from rich import box

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 5,
    "page": 1,
    "sparkline": False,
}

def fetch_volume_data():
    """Fetches volume data for cryptocurrencies from the CoinGecko API and returns it as a list."""
    try:
        response = requests.get(API_URL, params=PARAMS)
        if response.status_code == 200:
            volume_data = response.json()
            volume_list = []

            # Extract relevant data for each cryptocurrency
            for asset in volume_data:
                name = asset.get("name", "N/A")
                symbol = asset.get("symbol", "N/A").upper()
                current_price = asset.get("current_price", 0.0)
                volume = asset.get("total_volume", 0)
                percent_change = asset.get("price_change_percentage_24h", 0)
                
                volume_list.append([name, symbol, current_price, volume, percent_change])
                
            return volume_list
        else:
            print("Failed to fetch data. Please check the API.")
            return []
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def display_terminal_title(console):
    """Displays a styled title for the screener."""
    console.print(Panel("Volume Screener", expand=False, border_style="bold white", box=box.ROUNDED))

def display_volume_table(volume_data):
    """Displays volume data in a nicely formatted table."""
    console = Console()
    
    # Show terminal title
    display_terminal_title(console)
    
    # Define table with a bold header style
    header_style = Style(color="white", bold=True)
    table = Table(show_header=True, header_style=header_style, box=box.SIMPLE)
    
    table.add_column("Name", justify="left")
    table.add_column("Symbol", justify="center")
    table.add_column("Price (USD)", justify="right")
    table.add_column("Volume", justify="right")
    table.add_column("% Change (24h)", justify="right")
    
    # Populate the table with data
    for entry in volume_data:
        percent_change = f"{entry[4]:.2f}%"
        row_style = Style(color="green" if entry[4] > 0 else "red", bold=True)
        table.add_row(
            entry[0],  # Name
            entry[1],  # Symbol
            f"${entry[2]:,.2f}",  # Current Price
            f"{entry[3]:,}",  # Volume
            percent_change,  # 24h % Change
            style=row_style
        )
    
    # Display the table
    console.print(table)

def display_ascii_chart(volume_data):
    """Displays a simple ASCII chart of trading volumes with color coding."""
    symbols = [entry[1] for entry in volume_data]
    volumes = [entry[3] for entry in volume_data]

    fig = tpl.figure()
    fig.barh(volumes, symbols, force_ascii=True)
    fig.show()

def main():
    # Fetch data from the API
    volume_data = fetch_volume_data()
    
    if volume_data:
        # Display the fetched data in a table
        display_volume_table(volume_data)
        
        # Generate and display an ASCII bar chart
        display_ascii_chart(volume_data)
    else:
        print("No data found.")

if __name__ == "__main__":
    main()
