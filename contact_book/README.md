Contact Book (Local CLI Version)
A simple, command-line interface (CLI) based contact management system built with Python. This utility allows users to add, view, search for, and delete contacts, with all data persistently stored in a local JSON file. It's a great example of basic data management and user interaction in a console application.

🚀 Features
The contact_book offers the following functionalities:

Add New Contacts: Easily add new contacts with details such as name, phone number, and email address. Includes basic validation to prevent empty names and duplicate names (case-insensitive).

View All Contacts: Display a neatly formatted list of all stored contacts.

Search Contacts: Quickly find contacts by searching for their name (case-insensitive).

Delete Contacts: Remove unwanted contacts from the contact book by specifying their name.

Persistent Storage: All contact data is automatically saved to and loaded from a local contacts.json file, ensuring your contacts are preserved between sessions.

Menu-Driven Interface: User-friendly command-line menu for easy navigation and interaction.

⚙️ Key Concepts
This project demonstrates several fundamental Python programming concepts:

File Handling (JSON): Reading from and writing to JSON files (json module) for structured data storage and retrieval.

Data Structures: Using a list of dictionaries to represent and manage contact information.

User Input & Output: Interacting with the user via input() and print() for menu navigation and data entry.

Functions for Modularity: Breaking down the application into logical functions (e.g., add_contact, view_contacts, save_contacts).

Basic Input Validation: Ensuring minimal data quality (e.g., non-empty names).

Error Handling: Gracefully managing potential issues during file operations (e.g., json.JSONDecodeError).

📦 How to Run
Follow these steps to get the contact_book running on your local machine:

Navigate to the Module Directory:
Open your terminal or command prompt and change your current directory to algokit/contact_book/.

Bash

cd algokit/contact_book/
Ensure contacts.json Exists:
Make sure an empty contacts.json file exists in the same directory as main.py. If it doesn't, the script will create it automatically when you first add a contact. If you want to create it manually before running, it should contain an empty JSON array:

Bash

# On Windows PowerShell:
New-Item -Path contacts.json -ItemType File -Value "[]"

# On Linux/macOS:
touch contacts.json
echo "[]" > contacts.json
Run the Script:
Execute the main.py script directly:

Bash

python main.py
Interact with the Menu:
Once the script starts, you will see a menu of options. Enter the corresponding number to perform an action:

1. Add New Contact:

Prompts you for the contact's name, phone number, and email.

Example: Enter "John Doe", "123-456-7890", "john@example.com".

2. View All Contacts:

Displays a list of all contacts currently stored.

3. Search Contact:

Asks for a name (or part of a name) to search for.

4. Delete Contact:

Prompts for the name of the contact to delete.

5. Exit:

Closes the application. Your contacts will be saved and loaded automatically next time you run the script.

✅ Checkpoints & Evaluation
The contact_book module has been developed with several key capabilities in mind. Here's a detailed evaluation of each checkpoint:

1. Add Contacts
Status: PASS

Evaluation: Users can successfully input and add new contacts. The system prevents adding contacts with the exact same name (case-insensitive) to avoid basic duplicates.

Implementation Detail: add_contact function handles user input and appends new contact dictionaries to the list, saving to contacts.json.

2. View All Contacts
Status: PASS

Evaluation: The view_contacts function retrieves and displays all contacts in a clear, formatted manner.

Implementation Detail: Iterates through the loaded contacts list and prints details.

3. Search Contacts
Status: PASS

Evaluation: The search_contact function allows users to find contacts by entering a name. The search is case-insensitive and displays all matching entries.

Implementation Detail: Filters the contacts list based on the search term present in the contact's name.

4. Delete Contacts
Status: PASS

Evaluation: Users can specify a contact name to remove. The system deletes the contact (case-insensitive match) and updates the contacts.json file.

Implementation Detail: Creates a new list excluding the deleted contact and overwrites the old list.

5. Persistent Storage
Status: PASS

Evaluation: Contacts are automatically loaded from contacts.json when the application starts and saved back to the file after any modification (add, delete). This ensures data is not lost when the program closes.

Implementation Detail: load_contacts and save_contacts functions manage JSON file I/O.

6. Robustness & Error Handling
Status: PASS

Evaluation: The script includes basic error handling for file operations (e.g., json.JSONDecodeError if contacts.json is corrupted) and input validation (e.g., preventing empty names).

Implementation Detail: try-except blocks are used for file operations, and if not name.strip(): checks for empty inputs.

7. Cross-Platform Compatibility
Status: PASS

Evaluation: The module uses only Python's standard library features (os, json, logging), which are inherently cross-platform. It runs consistently on Windows, macOS, and Linux.

Implementation Detail: Relies on Python's built-in OS abstraction.