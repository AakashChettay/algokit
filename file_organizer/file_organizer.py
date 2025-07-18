# algokit/file_organizer/main.py
import os
import shutil
import argparse
import logging
import json
import datetime
import stat # For checking hidden attribute on Windows (though not fully robust for all hidden types)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Global variable for file categories, loaded from config
FILE_CATEGORIES = {}
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def load_categories_from_config():
    """
    Loads file category mappings from the config.json file.
    """
    global FILE_CATEGORIES
    if not os.path.exists(CONFIG_FILE):
        logging.error(f"Error: Configuration file '{CONFIG_FILE}' not found. Please create it.")
        # Provide a default minimal config if not found to prevent crash
        FILE_CATEGORIES = {
            'Documents': ['.pdf', '.txt'],
            'Others': []
        }
        return

    try:
        with open(CONFIG_FILE, 'r') as f:
            FILE_CATEGORIES = json.load(f)
        logging.info("File categories loaded from config.json.")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding config.json: {e}. Using default categories.")
        FILE_CATEGORIES = {
            'Documents': ['.pdf', '.txt'],
            'Others': []
        }
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading config: {e}. Using default categories.")
        FILE_CATEGORIES = {
            'Documents': ['.pdf', '.txt'],
            'Others': []
        }

def get_category(file_extension: str) -> str:
    """
    Determines the category of a file based on its extension using loaded configurations.

    Args:
        file_extension (str): The extension of the file (e.g., '.pdf', '.jpg').

    Returns:
        str: The name of the category (e.g., 'Documents', 'Images'), or 'Others' if not found.
    """
    file_extension = file_extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category
    return 'Others'

def is_hidden_or_system_file(file_path: str) -> bool:
    """
    Checks if a file is considered hidden or a system file.
    Handles Unix-like dot files and basic Windows hidden attribute.

    Args:
        file_path (str): The full path to the file.

    Returns:
        bool: True if the file is hidden/system, False otherwise.
    """
    file_name = os.path.basename(file_path)
    # Common hidden files on Unix-like systems
    if file_name.startswith('.'):
        return True

    # Basic check for Windows hidden attribute (not foolproof for all system files)
    if os.name == 'nt': # If OS is Windows
        try:
            # Check if the hidden attribute is set
            return bool(os.stat(file_path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        except AttributeError:
            # stat.FILE_ATTRIBUTE_HIDDEN might not exist on all Python versions/platforms,
            # but os.name == 'nt' implies it should. Fallback if not.
            pass
        except Exception as e:
            logging.debug(f"Could not check hidden attribute for '{file_name}': {e}")

    return False

def get_unique_filename(destination_path: str, original_filename: str) -> str:
    """
    Generates a unique filename to prevent overwriting.
    Appends a timestamp or a counter if the file already exists.

    Args:
        destination_path (str): The full path to the intended destination directory.
        original_filename (str): The original name of the file.

    Returns:
        str: A unique filename (e.g., 'report.pdf' or 'report_20250718_123456.pdf').
    """
    base_name, ext = os.path.splitext(original_filename)
    new_filename = original_filename
    counter = 1

    while os.path.exists(os.path.join(destination_path, new_filename)):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{base_name}_{timestamp}{ext}"
        # Fallback to simple counter if timestamp also clashes (highly unlikely)
        if os.path.exists(os.path.join(destination_path, new_filename)):
             new_filename = f"{base_name}_{counter}{ext}"
             counter += 1
        logging.warning(f"File '{original_filename}' already exists. Renaming to '{new_filename}'.")
    return new_filename


def organize_files(source_dir: str, dry_run: bool = False, recursive: bool = False):
    """
    Organizes files in the specified source directory (and optionally its subdirectories)
    into subfolders based on their file type/extension.

    Args:
        source_dir (str): The path to the directory to organize.
        dry_run (bool): If True, only simulate actions without moving files.
        recursive (bool): If True, process files in subdirectories as well.
    """
    if not os.path.isdir(source_dir):
        logging.error(f"Error: Source directory '{source_dir}' does not exist or is not a directory.")
        return

    logging.info(f"Starting file organization in: '{source_dir}' {'(DRY RUN)' if dry_run else ''}")
    if recursive:
        logging.info("Processing files recursively in subdirectories.")

    # Load categories at the start of the organization process
    load_categories_from_config()
    if not FILE_CATEGORIES:
        logging.error("No file categories loaded. Aborting organization.")
        return

    # Use os.walk for recursive processing, otherwise just listdir for flat processing
    for root, dirs, files in os.walk(source_dir):
        if not recursive and root != source_dir:
            # If not recursive, only process the top-level directory
            continue

        # Filter out hidden/system directories if processing recursively
        # (though os.walk typically skips some common system ones by default)
        dirs[:] = [d for d in dirs if not is_hidden_or_system_file(os.path.join(root, d))]

        for item in files:
            item_path = os.path.join(root, item)

            # Skip hidden/system files
            if is_hidden_or_system_file(item_path):
                logging.info(f"Skipping hidden/system file: '{item}'")
                continue

            # Get file extension
            file_name, file_extension = os.path.splitext(item)

            # Determine category and destination directory
            category = get_category(file_extension)
            destination_dir = os.path.join(source_dir, category) # Always move to a category folder in the ROOT source_dir

            # Ensure the destination directory is not the current source directory of the file
            # This prevents infinite loops if a category folder is inside a scanned subfolder
            if os.path.commonpath([destination_dir, root]) == root and root != source_dir:
                 logging.warning(f"Skipping move for '{item}' from '{root}' to '{destination_dir}' as destination is a subfolder of source root.")
                 continue

            # Create destination directory if it doesn't exist
            try:
                if dry_run:
                    logging.info(f"[DRY RUN] Would create directory: '{destination_dir}'")
                else:
                    os.makedirs(destination_dir, exist_ok=True)
            except OSError as e:
                logging.error(f"Error creating directory '{destination_dir}': {e}")
                continue # Skip moving this file if directory creation fails

            # Handle duplicate filenames
            final_item_name = get_unique_filename(destination_dir, item)
            destination_path = os.path.join(destination_dir, final_item_name)

            # Move the file
            if dry_run:
                logging.info(f"[DRY RUN] Would move '{item_path}' to '{destination_path}'")
            else:
                try:
                    shutil.move(item_path, destination_path)
                    logging.info(f"Moved '{item}' to '{os.path.relpath(destination_path, source_dir)}'")
                except shutil.Error as e:
                    logging.warning(f"Could not move '{item}' to '{os.path.relpath(destination_path, source_dir)}': {e}")
                except Exception as e:
                    logging.error(f"An unexpected error occurred while moving '{item}': {e}")

    logging.info("File organization complete.")

def main():
    """
    Main entry point for the file_organizer script.
    Parses command-line arguments to get the source directory, and options for dry run/recursion.
    """
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by type/extension."
    )
    parser.add_argument(
        "source_directory",
        type=str,
        help="The path to the directory you want to organize."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the organization process without actually moving files."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Organize files in subdirectories as well."
    )

    args = parser.parse_args()
    organize_files(args.source_directory, dry_run=args.dry_run, recursive=args.recursive)

if __name__ == "__main__":
    main()