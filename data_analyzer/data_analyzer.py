# algokit/data_analyser/main.py
import csv
import os
import logging
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_csv_data(file_path: str) -> list[dict]:
    """
    Loads data from a CSV file into a list of dictionaries.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list[dict]: A list where each dictionary represents a row,
                    with column headers as keys. Returns an empty list on error.
    """
    if not os.path.exists(file_path):
        logging.error(f"Error: File not found at '{file_path}'")
        return []
    
    data = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
        logging.info(f"Successfully loaded {len(data)} rows from '{file_path}'.")
        return data
    except Exception as e:
        logging.error(f"Error loading CSV file '{file_path}': {e}")
        return []

def print_data(data: list[dict]):
    """
    Prints the loaded data in a formatted way.
    """
    if not data:
        print("No data to display.")
        return

    # Get all unique headers from the data (handles cases where rows might have different keys)
    headers = []
    for row in data:
        for key in row.keys():
            if key not in headers:
                headers.append(key)
    
    if not headers:
        print("No headers found in data.")
        return

    # Determine max width for each column
    column_widths = {header: len(header) for header in headers}
    for row in data:
        for header in headers:
            column_widths[header] = max(column_widths[header], len(str(row.get(header, ''))))
    
    # Print header row
    header_line = " | ".join(f"{header:<{column_widths[header]}}" for header in headers)
    print("\n" + "=" * len(header_line))
    print(header_line)
    print("-" * len(header_line))

    # Print data rows
    for row in data:
        row_line = " | ".join(f"{str(row.get(header, '')):<{column_widths[header]}}" for header in headers)
        print(row_line)
    print("=" * len(header_line) + "\n")


# --- Handwritten Sorting Algorithm (Bubble Sort) ---
def bubble_sort(data: list[dict], column: str, reverse: bool = False) -> list[dict]:
    """
    Sorts a list of dictionaries (CSV rows) using the Bubble Sort algorithm.

    Args:
        data (list[dict]): The list of dictionaries to sort.
        column (str): The column name (key) to sort by.
        reverse (bool): If True, sort in descending order.

    Returns:
        list[dict]: The sorted list of dictionaries. Returns original data if column is invalid.
    """
    n = len(data)
    if n <= 1:
        return data # Already sorted or empty

    # Check if column exists in at least one row
    if not any(column in row for row in data):
        logging.error(f"Error: Column '{column}' not found in data for sorting.")
        return data # Return original data if column is invalid

    # Create a copy to avoid modifying the original list in place
    sorted_data = list(data)

    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            val1 = sorted_data[j].get(column, '')
            val2 = sorted_data[j + 1].get(column, '')

            # Attempt to convert to numeric for comparison if possible
            try:
                val1 = float(val1)
                val2 = float(val2)
            except ValueError:
                # If not numeric, compare as strings
                pass

            if (not reverse and val1 > val2) or (reverse and val1 < val2):
                sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]
                swapped = True
        if not swapped:
            break # No swaps in this pass, data is sorted

    logging.info(f"Data sorted by column '{column}' {'(descending)' if reverse else '(ascending)'} using Bubble Sort.")
    return sorted_data


# --- Handwritten Searching Algorithm (Linear Search) ---
def linear_search(data: list[dict], search_column: str, search_value: str) -> list[dict]:
    """
    Searches a list of dictionaries (CSV rows) using the Linear Search algorithm.

    Args:
        data (list[dict]): The list of dictionaries to search.
        search_column (str): The column name (key) to search within.
        search_value (str): The value to search for (case-insensitive for strings).

    Returns:
        list[dict]: A list of dictionaries (rows) that match the search criteria.
                    Returns empty list if column is invalid or no matches found.
    """
    found_rows = []
    
    # Check if search_column exists in at least one row
    if not any(search_column in row for row in data):
        logging.error(f"Error: Search column '{search_column}' not found in data for searching.")
        return []

    # Convert search_value to string for consistent comparison
    search_value_str = str(search_value).lower()

    for row in data:
        # Get the value from the specified column, default to empty string if not found
        column_value = str(row.get(search_column, '')).lower()
        
        if search_value_str in column_value: # Case-insensitive partial match
            found_rows.append(row)
            
    logging.info(f"Linear search completed for '{search_value}' in column '{search_column}'. Found {len(found_rows)} matches.")
    return found_rows


def main():
    """
    Main entry point for the Data Analyzer script.
    Handles command-line arguments for loading, sorting, and searching CSV data.
    """
    parser = argparse.ArgumentParser(
        description="AlgoKit Data Analyzer: Reads CSV files, sorts, and searches data using handwritten algorithms."
    )
    parser.add_argument(
        "csv_file",
        type=str,
        help="Path to the CSV file to analyze."
    )

    # Mutually exclusive group for sort or search operations
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--sort-by",
        type=str,
        help="Column name to sort the data by (ascending by default)."
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Sort in descending order (only applicable with --sort-by)."
    )

    group.add_argument(
        "--search-column",
        type=str,
        help="Column name to search within."
    )
    parser.add_argument(
        "--search-value",
        type=str,
        help="Value to search for within the specified column (case-insensitive partial match)."
    )

    args = parser.parse_args()

    # Load data first
    data = load_csv_data(args.csv_file)
    if not data:
        return # Exit if data loading failed

    if args.sort_by:
        print(f"\n--- Sorting Data by '{args.sort_by}' {'(Descending)' if args.reverse else '(Ascending)'} ---")
        sorted_data = bubble_sort(data, args.sort_by, args.reverse)
        print_data(sorted_data)
    elif args.search_column and args.search_value is not None:
        print(f"\n--- Searching for '{args.search_value}' in column '{args.search_column}' ---")
        search_results = linear_search(data, args.search_column, args.search_value)
        print_data(search_results)
    else:
        # If no specific operation, just print the loaded data
        print("\n--- Loaded Data ---")
        print_data(data)
        print("\nUse --sort-by or --search-column/--search-value for analysis.")
        parser.print_help()


if __name__ == "__main__":
    main()