import os
import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.text import Text
from rich.panel import Panel
import random

def list_csv_files(directory):
    """List all CSV files in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith('.csv')]

def select_csv_file():
    """Prompt the user to select a CSV file from the output directory."""
    output_directory = "output"
    csv_files = list_csv_files(output_directory)
    
    if not csv_files:
        print("No CSV files found in the 'output' directory.")
        return None
    
    print("Available CSV files:")
    for idx, file in enumerate(csv_files):
        print(f"{idx + 1}. {file}")
    
    # Get user's choice
    while True:
        try:
            choice = int(input(f"Select a file (1-{len(csv_files)}): "))
            if 1 <= choice <= len(csv_files):
                selected_file = os.path.join(output_directory, csv_files[choice - 1])
                print(f"Selected file: {csv_files[choice - 1]}")
                return selected_file
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def load_data(world_market_file):
    """Load data from the specified CSV file."""
    if os.path.exists(world_market_file):
        df = pd.read_csv(world_market_file)
        return df
    else:
        print(f"{world_market_file} not found.")
        return None

def convert_market_cap_to_numeric(market_cap_str):
    """Converts market cap strings like '3.5 T' or '500 B' to float values."""
    market_cap_str = market_cap_str.replace('$', '').strip()
    if 'T' in market_cap_str:
        return float(market_cap_str.replace('T', '')) * 1e12
    elif 'B' in market_cap_str:
        return float(market_cap_str.replace('B', '')) * 1e9
    elif 'M' in market_cap_str:
        return float(market_cap_str.replace('M', '')) * 1e6
    else:
        return float(market_cap_str)  # Assuming it's a plain number

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
    gradient_colors = generate_gradient_color(start_color, end_color, len("Screener"))
    title_text = Text()

    # Apply gradient to each letter
    for idx, char in enumerate("Screener"):
        color = gradient_colors[idx]
        title_text.append(char, style=Style(color=color, bold=True))
    
    # Create a larger title using a Panel for emphasis
    console.print(Panel(title_text, expand=False, border_style="bold white"))

def display_table(data):
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
    
    table.add_column("Rank", justify="center")
    table.add_column("Name", justify="left")
    table.add_column("Market Cap", justify="right")
    table.add_column("Price", justify="right")
    table.add_column("Country", justify="center")
    
    # Display the first 50 rows with gradient color
    for idx, (_, row) in enumerate(data.head(50).iterrows()):
        row_style = Style(color=gradient_colors[idx], bold=True)
        table.add_row(
            str(row['Rank']),
            row['Name'],
            row['Market Cap'],
            row['Price'],
            row['Country'],
            style=row_style
        )
    
    console.print(table)

def display_focus_window(data, start_color, end_color):
    # Pick a random company from the data
    random_company = data.sample(n=1).iloc[0]
    company_details = [
        f"Company: {random_company['Name']}",
        f"Rank: {random_company['Rank']}",
        f"Market Cap: {random_company['Market Cap']}",
        f"Price: {random_company['Price']}",
        f"Country: {random_company['Country']}"
    ]

    # Generate gradient colors for the company details
    gradient_colors = generate_gradient_color(start_color, end_color, len(company_details))
    details_text = Text()

    # Apply gradient colors to each line of company details
    for idx, detail in enumerate(company_details):
        color = gradient_colors[idx]
        details_text.append(detail + "\n", style=Style(color=color, bold=True))
    
    # Create a panel with the gradient-colored company details
    console = Console()
    console.print(Panel(details_text, title="Company Details", border_style="bold white", width=73))

def display_chart(data):
    # Convert market cap to numeric values
    data['Market Cap (Numeric)'] = data['Market Cap'].apply(convert_market_cap_to_numeric)
    # Sort by Market Cap in descending order and take the top 50 companies
    sorted_data = data.sort_values(by='Market Cap (Numeric)', ascending=False).head(50)
    
    # Prepare labels for the chart
    sorted_data['Label'] = sorted_data.apply(lambda x: f"{x['Name']} ({x['Market Cap']}, {x['Country']})", axis=1)
    
    # Generate a vertical bar chart
    plt.figure(figsize=(10, 15))
    plt.barh(sorted_data['Label'], sorted_data['Market Cap (Numeric)'], color='blue')
    plt.gca().invert_yaxis()  # Largest at the top
    plt.xlabel('Market Cap (in USD)')
    plt.title('Top 50 Companies by Market Cap')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.show()

def main():
    # Prompt the user to select a CSV file
    selected_file = select_csv_file()
    
    if selected_file:
        data = load_data(selected_file)
        
        if data is not None:
            display_table(data)  # Now showing 50 companies
            
            # Define the start and end colors for the gradient
            start_color = (30, 144, 255)  # Light blue
            end_color = (255, 69, 0)      # Red

            # Show a random company in a focus window
            display_focus_window(data, start_color, end_color)
            
            print("\nGenerating chart...")
            display_chart(data)
        else:
            print("No data found. Please ensure the selected CSV file is valid.")
    else:
        print("No file selected. Exiting.")

if __name__ == "__main__":
    main()
