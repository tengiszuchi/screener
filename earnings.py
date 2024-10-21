import requests
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.text import Text
from rich.panel import Panel

# Alpha Vantage free API endpoint - Requires a valid API key (get it from https://www.alphavantage.co)
BASE_URL = "https://www.alphavantage.co/query"
API_KEY = "YOUR_API_KEY"  # Replace with your actual Alpha Vantage API key

def fetch_earnings_data(symbol="AAPL"):
    """Fetches earnings data for a specific symbol from the Alpha Vantage API."""
    params = {
        "function": "EARNINGS",
        "symbol": symbol,
        "apikey": API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            earnings_list = []
            
            # Parse the quarterly earnings data
            if "quarterlyEarnings" in data:
                for report in data["quarterlyEarnings"]:
                    company = symbol
                    report_date = report.get("fiscalDateEnding", "N/A")
                    eps_estimate = report.get("estimatedEPS", "N/A")
                    eps_actual = report.get("reportedEPS", "N/A")
                    
                    earnings_list.append([company, report_date, eps_estimate, eps_actual])
            
            return earnings_list
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
    gradient_colors = generate_gradient_color(start_color, end_color, len("Earnings Screener"))
    title_text = Text()

    # Apply gradient to each letter
    for idx, char in enumerate("Earnings Screener"):
        color = gradient_colors[idx]
        title_text.append(char, style=Style(color=color, bold=True))
    
    # Create a larger title using a Panel for emphasis
    console.print(Panel(title_text, expand=False, border_style="bold white"))

def display_earnings_table(earnings_data):
    """Displays earnings data in a nicely formatted table."""
    console = Console()
    
    # Define the start and end colors for the gradient
    start_color = (30, 144, 255)  # Light blue
    end_color = (255, 69, 0)      # Red
    
    # Show terminal title with gradient
    display_terminal_title(console, start_color, end_color)
    
    # Generate a gradient list based on the number of rows to display
    gradient_colors = generate_gradient_color(start_color, end_color, len(earnings_data))
    
    # Define table with a bold header style
    header_style = Style(color="white", bold=True)
    table = Table(show_header=True, header_style=header_style)
    
    table.add_column("Company", justify="left")
    table.add_column("Report Date", justify="center")
    table.add_column("EPS Estimate", justify="right")
    table.add_column("EPS Actual", justify="right")
    
    # Populate the table with data, applying gradient colors to rows
    for idx, entry in enumerate(earnings_data):
        row_style = Style(color=gradient_colors[idx % len(gradient_colors)], bold=True)
        table.add_row(
            entry[0],  # Company Name
            entry[1],  # Report Date
            f"{entry[2]}" if entry[2] != "N/A" else "N/A",  # EPS Estimate
            f"{entry[3]}" if entry[3] != "N/A" else "N/A",  # EPS Actual
            style=row_style
        )
    
    # Display the table
    console.print(table)

def main():
    # Fetch data for a specific company (e.g., Apple Inc.)
    earnings_data = fetch_earnings_data(symbol="AAPL")
    
    if earnings_data:
        # Display the fetched data in a table
        display_earnings_table(earnings_data)
    else:
        print("No data found.")

if __name__ == "__main__":
    main()
