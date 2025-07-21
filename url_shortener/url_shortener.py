# algokit/url_shortener/main.py
import os
import json
import argparse
import random
import string
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# File to store URL mappings
STORAGE_FILE = os.path.join(os.path.dirname(__file__), 'urls.json')

def load_urls() -> dict:
    """
    Loads URL mappings from the JSON storage file.

    Returns:
        dict: A dictionary mapping short codes to long URLs.
    """
    if not os.path.exists(STORAGE_FILE):
        return {}
    try:
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error reading {STORAGE_FILE}: {e}. Starting with empty mappings.")
        return {}
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading URLs: {e}. Starting with empty mappings.")
        return {}

def save_urls(urls: dict):
    """
    Saves URL mappings to the JSON storage file.

    Args:
        urls (dict): The dictionary of URL mappings to save.
    """
    try:
        with open(STORAGE_FILE, 'w') as f:
            json.dump(urls, f, indent=4)
        logging.info(f"URL mappings saved to {STORAGE_FILE}.")
    except Exception as e:
        logging.error(f"Error saving URLs to {STORAGE_FILE}: {e}")

def generate_short_code(long_url: str, length: int = 6) -> str:
    """
    Generates a unique short code for a given long URL.
    Uses a combination of hashing and random characters to enhance uniqueness.

    Args:
        long_url (str): The original URL to shorten.
        length (int): Desired length of the short code.

    Returns:
        str: A unique short code.
    """
    # Simple hash of the URL
    url_hash = hashlib.sha256(long_url.encode('utf-8')).hexdigest()[:length].upper()

    # Add some random characters to further reduce collision chances
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length // 2))

    # Combine them, ensuring the target length
    short_code = (url_hash + random_chars)[:length]

    # Ensure uniqueness by checking existing codes (simple linear probe for demo)
    urls = load_urls()
    while short_code in urls:
        logging.warning(f"Generated code '{short_code}' already exists. Regenerating...")
        short_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    return short_code

def shorten_url(long_url: str) -> str:
    """
    Shortens a given long URL, stores the mapping, and returns the short code.

    Args:
        long_url (str): The original URL to shorten.

    Returns:
        str: The generated short code, or None if an error occurs.
    """
    if not long_url.strip():
        logging.error("Long URL cannot be empty.")
        return None

    urls = load_urls()

    # Check if URL is already shortened
    for code, url in urls.items():
        if url == long_url:
            logging.info(f"URL already shortened: {long_url} -> {code}")
            return code

    short_code = generate_short_code(long_url)
    urls[short_code] = long_url
    save_urls(urls)
    logging.info(f"URL shortened: {long_url} -> {short_code}")
    return short_code

def expand_url(short_code: str) -> str:
    """
    Expands a given short code to retrieve the original long URL.

    Args:
        short_code (str): The short code to expand.

    Returns:
        str: The original long URL, or None if the short code is not found.
    """
    if not short_code.strip():
        logging.error("Short code cannot be empty.")
        return None

    urls = load_urls()
    long_url = urls.get(short_code)
    if long_url:
        logging.info(f"Expanded: {short_code} -> {long_url}")
        return long_url
    else:
        logging.warning(f"Short code '{short_code}' not found.")
        return None

def main():
    """
    Main entry point for the URL Shortener script.
    Handles command-line arguments for shortening and expanding URLs.
    """
    parser = argparse.ArgumentParser(
        description="URL Shortener: Generates short codes for long URLs and expands them."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--shorten",
        type=str,
        help="The long URL to shorten."
    )
    group.add_argument(
        "--expand",
        type=str,
        help="The short code to expand."
    )

    args = parser.parse_args()

    if args.shorten:
        short_code = shorten_url(args.shorten)
        if short_code:
            print(f"Shortened URL: {short_code}")
    elif args.expand:
        long_url = expand_url(args.expand)
        if long_url:
            print(f"Original URL: {long_url}")
        else:
            print(f"Error: Short code '{args.expand}' not found.")

if __name__ == "__main__":
    main()