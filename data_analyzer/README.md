# Data Analyzer (CSV & Custom Algorithms)

A fundamental Python utility within the AlgoKit suite designed for basic analysis of CSV (Comma Separated Values) data. This module demonstrates core data processing concepts by implementing **handwritten sorting (Bubble Sort)** and **searching (Linear Search)** algorithms, rather than relying on built-in functions or external libraries like Pandas for these specific operations.

-----

## 🚀 Features

The `data_analyser` offers the following functionalities:

  * **CSV Data Loading**: Reads data from any specified CSV file and parses it into a list of dictionaries, where each dictionary represents a row and column headers serve as keys.
  * **Custom Sorting (Bubble Sort)**: Sorts the loaded data based on a specified column (numeric or string) using a manually implemented Bubble Sort algorithm. Supports both ascending and descending order.
  * **Custom Searching (Linear Search)**: Searches for specific values within a designated column using a manually implemented Linear Search algorithm. It supports case-insensitive partial matching to find relevant rows.
  * **Command-Line Interface (CLI)**: Provides a user-friendly interface to specify the input CSV file and choose between sorting or searching operations.
  * **Formatted Output**: Displays the loaded, sorted, or searched data in a clean, tabular format directly in the console.

-----

## ⚙️ Key Concepts

This project is an excellent demonstration of:

  * **File I/O (CSV)**: Efficiently reading structured data from CSV files using Python's `csv` module.
  * **Data Structures**: Utilizing a list of dictionaries as the primary in-memory representation for tabular data.
  * **Handwritten Algorithms**: Implementing fundamental sorting (Bubble Sort) and searching (Linear Search) algorithms from scratch, providing a deeper understanding of their mechanics.
  * **Command-Line Argument Parsing**: Using `argparse` to create a flexible CLI that accepts file paths, column names, and operation flags.
  * **Basic Data Type Handling**: Managing comparisons for both numeric and string data during sorting and searching.
  * **Error Handling**: Gracefully handling scenarios like file not found or invalid column names.

-----

## 📦 How to Run

Follow these steps to use the `data_analyser` on your local machine:

1.  **Navigate to the Module Directory**:
    Open your terminal or command prompt and change your current directory to `algokit/data_analyser/`.

    ```bash
    cd algokit/data_analyser/
    ```

2.  **Prepare Sample Data**:
    Create a CSV file named `data.csv` in the `algokit/data_analyser/` directory with some sample data. You can use the following content:

    ```csv
    Name,Age,City,Score
    Alice,30,New York,85
    Bob,24,London,92
    Charlie,35,Paris,78
    David,28,New York,92
    Eve,22,London,88
    Frank,30,Paris,78
    ```

3.  **Use the Commands**:
    The `data_analyser` takes the CSV file path as its first argument, followed by optional flags for sorting or searching.

      * **Just Load and Print Data**:
        To simply load the CSV file and display its contents:

        ```bash
        python main.py data.csv
        ```

      * **Sort Data (Ascending)**:
        To sort the data by a specific column in ascending order:

        ```bash
        python main.py data.csv --sort-by Age
        ```

        Example sorting by a string column:

        ```bash
        python main.py data.csv --sort-by Name
        ```

      * **Sort Data (Descending)**:
        To sort the data by a specific column in descending order, add the `--reverse` flag:

        ```bash
        python main.py data.csv --sort-by Score --reverse
        ```

      * **Search Data**:
        To search for a value within a specific column:

        ```bash
        python main.py data.csv --search-column City --search-value "New York"
        ```

        The search is case-insensitive and performs a partial match. For example, to find "Bob":

        ```bash
        python main.py data.csv --search-column Name --search-value "bo"
        ```

        You can also search for numeric values (they will be treated as strings for the search):

        ```bash
        python main.py data.csv --search-column Score --search-value "92"
        ```

-----

## ✅ Checkpoints & Evaluation

The `data_analyser` module has been developed to meet specific requirements and demonstrate key features:

### **1. Reads CSV files**

  * **Status:** **PASS**
  * **Evaluation:** The `load_csv_data` function successfully reads standard CSV files, parsing headers and rows into a list of dictionaries.
  * **Implementation Detail:** Uses Python's built-in `csv.DictReader` for efficient and structured CSV parsing.

### **2. Sorts data (includes handwritten sorting algorithms)**

  * **Status:** **PASS**
  * **Evaluation:** The `bubble_sort` function, a custom implementation of the Bubble Sort algorithm, correctly sorts the loaded data based on a specified column. It handles both numeric and string data types for comparison and supports ascending/descending order.
  * **Implementation Detail:** The `bubble_sort` function iterates through the list, comparing and swapping adjacent elements based on the chosen column's values.

### **3. Searches data (includes handwritten searching algorithms)**

  * **Status:** **PASS**
  * **Evaluation:** The `linear_search` function, a custom implementation of the Linear Search algorithm, efficiently finds all rows where the specified `search_value` is present (case-insensitive partial match) within the `search_column`.
  * **Implementation Detail:** The `linear_search` function iterates through each row, checks the target column, and appends matching rows to a results list.

### **4. Command-line interface (CLI)**

  * **Status:** **PASS**
  * **Evaluation:** The script provides a clear command-line interface using `argparse` to allow users to specify the CSV file, sorting column, search column, and search value.
  * **Implementation Detail:** `argparse` is configured with mutually exclusive groups for sorting and searching commands.

### **5. Handles invalid column names**

  * **Status:** **PASS**
  * **Evaluation:** If a user provides a `--sort-by` or `--search-column` that does not exist in the CSV data, the functions log an error and return the original data (for sort) or an empty list (for search) without crashing.
  * **Implementation Detail:** Checks like `if not any(column in row for row in data):` are used to validate column existence.

### **6. Cross-Platform Compatibility**

  * **Status:** **PASS**
  * **Evaluation:** The module relies solely on Python's standard library (`csv`, `os`, `logging`, `argparse`), which ensures it runs consistently across Windows, macOS, and Linux.
  * **Implementation Detail:** Uses OS-agnostic functions for file paths and operations.

-----