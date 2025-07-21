# URL Shortener (Local Script Version)

A straightforward Python utility that allows you to shorten long URLs and expand short codes locally. This tool demonstrates the core logic of a URL shortener using a simple file-based storage mechanism, without requiring any web server or database setup.

-----

## 🚀 Features

  * **Generate Short Codes**: Create unique, short alphanumeric codes for any long URL.
  * **Local Storage**: All URL mappings (short code to long URL) are persistently stored in a local JSON file (`urls.json`).
  * **Expand Short Codes**: Retrieve the original long URL from a given short code.
  * **Simulated Short URL**: Generates a full "short URL" string (e.g., `http://algok.it/ABCDEF`) to demonstrate how a real shortener would present its output, even though it's not a live web service.
  * **Command-Line Interface (CLI)**: Easy to use via simple commands in your terminal.

-----

## ⚙️ Key Concepts

This project illustrates fundamental Python concepts:

  * **File I/O**: Reading from and writing to JSON files for data persistence.
  * **String Manipulation**: Generating and processing short codes.
  * **Hashing & Randomness**: Using `hashlib` and `random` for unique code generation.
  * **Command-Line Arguments**: Utilizing `argparse` to handle user input for shortening and expanding.
  * **Basic Data Structures**: Using Python dictionaries to store key-value (short code: long URL) mappings.

-----

## 📦 How to Run

Follow these steps to get the URL Shortener running on your local machine:

1.  **Navigate to the Module Directory**:
    Open your terminal or command prompt and change your current directory to `algokit/url_shortener/`.

    ```bash
    cd algokit/url_shortener/
    ```

2.  **Ensure `urls.json` Exists**:
    Make sure an empty `urls.json` file exists in the same directory as `main.py`. If it doesn't, you can create it manually:

    ```bash
    # On Windows PowerShell:
    New-Item -Path urls.json -ItemType File -Value "{}"

    # On Linux/macOS:
    touch urls.json
    echo "{}" > urls.json
    ```

    The script will manage this file for storing your URL mappings.

3.  **Run the Script to Shorten a URL**:
    Use the `--shorten` argument followed by the long URL you want to shorten.

    ```bash
    python main.py --shorten "https://www.google.com/search?q=python+url+shortener+project+example&oq=python+url+shortener+project+example"
    ```

    The script will output a generated short URL string, like:

    ```
    Generated Short URL: http://algok.it/ABCDEF
    ```

    You can then check the `urls.json` file; it will now contain an entry mapping the generated code (`ABCDEF`) to your long URL.

4.  **Run the Script to Expand a Short URL**:
    Use the `--expand` argument followed by either the full short URL string or just the short code.

      * **Using the full short URL string:**
        ```bash
        python main.py --expand "http://algok.it/ABCDEF"
        ```
      * **Using just the short code:**
        ```bash
        python main.py --expand "ABCDEF"
        ```

    In both cases, the script will output the original long URL:

    ```
    Original URL: https://www.google.com/search?q=python+url+shortener+project+example&oq=python+url+shortener+project+example
    ```

5.  **Test Non-Existent Short Code**:

    ```bash
    python main.py --expand "NONEXIST"
    ```

    This will result in an error message indicating the code was not found.

-----

## ⚠️ Important Note on "Browser Expansion"

This `URL Shortener (Local Script Version)` is a **demonstration of the core logic**, not a live web service.

  * The "Short URL" generated (e.g., `http://algok.it/ABCDEF`) is a **simulated string**. You **cannot** paste this URL directly into a web browser and expect it to redirect.
  * For a real URL shortener that works in a browser, a web server needs to be running at the `algok.it` domain (or your chosen domain) to receive browser requests and perform the actual redirection. Our script handles the *lookup* part of that process locally.
