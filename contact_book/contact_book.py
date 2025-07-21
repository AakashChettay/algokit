# algokit/contact_book/main.py
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# File to store contacts
CONTACTS_FILE = os.path.join(os.path.dirname(__file__), 'contacts.json')

def load_contacts() -> list:
    """
    Loads contacts from the JSON storage file.

    Returns:
        list: A list of contact dictionaries. Returns an empty list if the file
              doesn't exist or is invalid.
    """
    if not os.path.exists(CONTACTS_FILE):
        logging.info("Contacts file not found. Starting with an empty contact list.")
        return []
    try:
        with open(CONTACTS_FILE, 'r') as f:
            contacts = json.load(f)
            if not isinstance(contacts, list):
                logging.warning("Contacts file content is not a list. Starting with empty list.")
                return []
            logging.info(f"Loaded {len(contacts)} contacts from {CONTACTS_FILE}.")
            return contacts
    except json.JSONDecodeError as e:
        logging.error(f"Error reading {CONTACTS_FILE}: {e}. File might be corrupted. Starting with empty list.")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading contacts: {e}. Starting with empty list.")
        return []

def save_contacts(contacts: list):
    """
    Saves the current list of contacts to the JSON storage file.

    Args:
        contacts (list): The list of contact dictionaries to save.
    """
    try:
        with open(CONTACTS_FILE, 'w') as f:
            json.dump(contacts, f, indent=4)
        logging.info(f"Saved {len(contacts)} contacts to {CONTACTS_FILE}.")
    except Exception as e:
        logging.error(f"Error saving contacts to {CONTACTS_FILE}: {e}")

def add_contact(contacts: list):
    """
    Prompts the user for contact details and adds a new contact to the list.
    Checks for duplicate names (case-insensitive).

    Args:
        contacts (list): The list of contact dictionaries to modify.
    """
    print("\n--- Add New Contact ---")
    name = input("Enter contact name: ").strip()
    if not name:
        print("Name cannot be empty. Contact not added.")
        return

    # Check for duplicate name (case-insensitive)
    for contact in contacts:
        if contact['name'].lower() == name.lower():
            print(f"Contact with name '{name}' already exists. Please use a unique name.")
            return

    phone = input("Enter phone number (optional): ").strip()
    email = input("Enter email address (optional): ").strip()

    new_contact = {
        'name': name,
        'phone': phone,
        'email': email
    }
    contacts.append(new_contact)
    save_contacts(contacts)
    print(f"Contact '{name}' added successfully! ✅")

def view_contacts(contacts: list):
    """
    Displays all contacts in the list.
    """
    print("\n--- Your Contacts ---")
    if not contacts:
        print("No contacts found. Add some first!")
        return

    for i, contact in enumerate(contacts):
        print(f"--- Contact {i + 1} ---")
        print(f"Name: {contact.get('name', 'N/A')}")
        print(f"Phone: {contact.get('phone', 'N/A')}")
        print(f"Email: {contact.get('email', 'N/A')}")
        print("-" * 20) # Separator

def search_contact(contacts: list):
    """
    Prompts the user for a search term and displays matching contacts by name.
    """
    print("\n--- Search Contacts ---")
    search_term = input("Enter name to search for: ").strip().lower()
    if not search_term:
        print("Search term cannot be empty.")
        return

    found_contacts = [
        contact for contact in contacts
        if search_term in contact['name'].lower()
    ]

    if not found_contacts:
        print(f"No contacts found matching '{search_term}'.")
        return

    print(f"\n--- Search Results for '{search_term}' ---")
    for i, contact in enumerate(found_contacts):
        print(f"--- Result {i + 1} ---")
        print(f"Name: {contact.get('name', 'N/A')}")
        print(f"Phone: {contact.get('phone', 'N/A')}")
        print(f"Email: {contact.get('email', 'N/A')}")
        print("-" * 20)

def delete_contact(contacts: list):
    """
    Prompts the user for a contact name and deletes it from the list.
    Handles case-insensitive matching.
    """
    print("\n--- Delete Contact ---")
    name_to_delete = input("Enter the name of the contact to delete: ").strip()
    if not name_to_delete:
        print("Name cannot be empty. No contact deleted.")
        return

    original_count = len(contacts)
    # Filter out contacts matching the name (case-insensitive)
    updated_contacts = [
        contact for contact in contacts
        if contact['name'].lower() != name_to_delete.lower()
    ]

    if len(updated_contacts) < original_count:
        print(f"Contact '{name_to_delete}' deleted successfully! 🗑️")
        contacts[:] = updated_contacts # Modify the original list in place
        save_contacts(contacts)
    else:
        print(f"Contact '{name_to_delete}' not found.")

def display_menu():
    """
    Displays the main menu options to the user.
    """
    print("\n--- Contact Book Menu ---")
    print("1. Add New Contact")
    print("2. View All Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")
    print("-------------------------")

def main():
    """
    Main function for the Contact Book application.
    Runs the menu loop and calls appropriate functions based on user input.
    """
    contacts = load_contacts() # Load contacts at the start of the application

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            view_contacts(contacts)
        elif choice == '3':
            search_contact(contacts)
        elif choice == '4':
            delete_contact(contacts)
        elif choice == '5':
            print("Exiting Contact Book. Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
        
        input("\nPress Enter to continue...") # Pause for user to read output

if __name__ == "__main__":
    main()