import os
import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.text import Text
from rich.panel import Panel
import seaborn as sns

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

def load_data(csv_file):
    """Load data from the specified CSV file."""
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        return df
    else:
        print(f"{csv_file} not found.")
        return None

def convert_market_cap_to_numeric(market_cap_str):
    """Convert market cap strings like '$3.5B' or '500M' to float values."""
    if isinstance(market_cap_str, str):
        market_cap_str = market_cap_str.replace('$', '').strip()
        if 'B' in market_cap_str:
            return float(market_cap_str.replace('B', '')) * 1e9
        elif 'M' in market_cap_str:
            return float(market_cap_str.replace('M', '')) * 1e6
        elif 'T' in market_cap_str:
            return float(market_cap_str.replace('T', '')) * 1e12
        else:
            return float(market_cap_str)  # Assuming it's a plain number
    return market_cap_str

def clean_and_convert_data(data):
    """Clean and convert specific columns to numeric values."""
    if 'Market Cap' in data.columns:
        data['Market Cap'] = data['Market Cap'].apply(convert_market_cap_to_numeric)
    if 'Price' in data.columns:
        data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
    return data

def select_columns(data):
    """Prompt the user to select columns for the correlation matrix."""
    print("\nAvailable Columns:")
    columns = list(data.columns)
    for idx, col in enumerate(columns):
        print(f"{idx + 1}. {col}")
    
    selected_columns = []
    while True:
        user_input = input("Select columns to include in the analysis (comma-separated numbers, e.g., 1,3,5): ")
        try:
            indices = [int(x) - 1 for x in user_input.split(',')]
            selected_columns = [columns[i] for i in indices if i < len(columns)]
            if selected_columns:
                print(f"Selected Columns: {selected_columns}")
                numeric_data = data[selected_columns].select_dtypes(include=['float64', 'int64'])
                return numeric_data
            else:
                print("No valid columns selected. Please try again.")
        except ValueError:
            print("Please enter valid column indices.")

def generate_correlation_matrix(data):
    """Generate a correlation matrix from the data, using only numeric columns."""
    if data.empty:
        print("No numeric data available for correlation analysis.")
        return None
    
    correlation_matrix = data.corr()
    return correlation_matrix

def display_correlation_table(correlation_matrix):
    """Displays the correlation matrix in a nicely formatted table."""
    if correlation_matrix is None:
        print("Correlation matrix is empty. No data to display.")
        return

    console = Console()
    
    # Define the start and end colors for the gradient
    start_color = (30, 144, 255)  # Light blue
    end_color = (255, 69, 0)      # Red
    
    # Generate gradient for the title text
    gradient_colors = generate_gradient_color(start_color, end_color, len("Correlation Screener"))
    title_text = Text()
    for idx, char in enumerate("Correlation Screener"):
        color = gradient_colors[idx]
        title_text.append(char, style=Style(color=color, bold=True))
    
    console.print(Panel(title_text, expand=False, border_style="bold white"))
    
    # Create a table for displaying the correlation matrix
    header_style = Style(color="white", bold=True)
    table = Table(show_header=True, header_style=header_style)
    
    # Add columns based on the asset names
    asset_names = correlation_matrix.columns
    table.add_column("Asset", justify="left")
    for name in asset_names:
        table.add_column(name, justify="center")
    
    # Populate the table with correlation data
    for i, row in enumerate(correlation_matrix.iterrows()):
        row_data = [asset_names[i]] + [f"{value:.2f}" for value in row[1]]
        row_style = Style(color="white" if i % 2 == 0 else "light_gray", bold=True)
        table.add_row(*row_data, style=row_style)
    
    console.print(table)

def generate_heatmap(data):
    """Generate a heatmap of the correlation matrix."""
    if data is None:
        print("Correlation matrix is empty. No data to visualize.")
        return
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(data, annot=True, cmap='coolwarm', center=0, linewidths=1, linecolor='white')
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()

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
    # Prompt the user to select a CSV file
    selected_file = select_csv_file()
    
    if selected_file:
        data = load_data(selected_file)
        
        if data is not None:
            # Clean and convert necessary columns to numeric values
            data = clean_and_convert_data(data)
            
            # Let the user choose which columns to include in the analysis
            selected_data = select_columns(data)
            
            # Generate correlation matrix
            correlation_matrix = generate_correlation_matrix(selected_data)
            
            # Display correlation table
            display_correlation_table(correlation_matrix)
            
            # Generate and show heatmap
            print("\nGenerating correlation heatmap...")
            generate_heatmap(correlation_matrix)
        else:
            print("No data found. Please ensure the selected CSV file is valid.")
    else:
        print("No file selected. Exiting.")

if __name__ == "__main__":
    main()
