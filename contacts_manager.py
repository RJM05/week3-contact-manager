# Contact Management System
# Developed by: Raja Mandal
# Architecture: Single Responsibility Principle (SRP) applied

import json
import re
import os
from datetime import datetime

# ==========================================
# 1. DATA LAYER (Persistence)
# Responsible ONLY for reading and writing files
# ==========================================
def load_contacts(filename="contacts_data.json"):
    """Loads contacts from a JSON file. Returns an empty dict if file doesn't exist."""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {} # Return empty if file is corrupted
    return {}

def save_contacts(contacts, filename="contacts_data.json"):
    """Saves the contacts dictionary to a JSON file with formatting."""
    with open(filename, 'w') as file:
        json.dump(contacts, file, indent=4)

# ==========================================
# 2. VALIDATION LAYER
# Responsible ONLY for checking data formatting
# ==========================================
def validate_phone(phone):
    """Strips non-digits and checks if length is 10-15."""
    # re.sub replaces any non-digit character (\D) with nothing ('')
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None

def validate_email(email):
    """Validates email format. Returns True if empty (since it's optional)."""
    if not email: 
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# ==========================================
# 3. BUSINESS LOGIC LAYER (CRUD Operations)
# Responsible ONLY for manipulating the dictionary
# ==========================================
def add_contact(contacts):
    print("\n--- ADD NEW CONTACT ---")
    name = input("Enter contact name: ").strip()
    
    if not name:
        print("❌ Name cannot be empty.")
        return
    if name in contacts:
        print(f"❌ Contact '{name}' already exists! Use the update option instead.")
        return

    # Phone input and validation loop
    phone = input("Enter phone number: ").strip()
    is_valid, cleaned_phone = validate_phone(phone)
    while not is_valid:
        print("❌ Invalid phone number. Please enter 10-15 digits.")
        phone = input("Enter phone number: ").strip()
        is_valid, cleaned_phone = validate_phone(phone)

    # Email input and validation loop
    email = input("Enter email (optional, press Enter to skip): ").strip()
    while not validate_email(email):
        print("❌ Invalid email format.")
        email = input("Enter email: ").strip()

    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other"

    # Create nested dictionary for the contact
    contacts[name] = {
        'phone': cleaned_phone,
        'email': email if email else None,
        'group': group,
        'updated_at': datetime.now().isoformat()
    }
    print(f"✅ Contact '{name}' added successfully!")
    save_contacts(contacts)

def search_contacts(contacts, search_term):
    """Returns a dictionary of contacts that partially match the search term."""
    search_term = search_term.lower()
    results = {}
    for name, info in contacts.items():
        if search_term in name.lower():
            results[name] = info
    return results

def update_contact(contacts):
    name = input("\nEnter the exact name of the contact to update: ").strip()
    if name not in contacts:
        print(f"❌ Contact '{name}' not found.")
        return

    print(f"Updating '{name}'. Press Enter to keep current values.")
    
    phone = input(f"Enter new phone [{contacts[name]['phone']}]: ").strip()
    if phone:
        is_valid, cleaned_phone = validate_phone(phone)
        if is_valid:
            contacts[name]['phone'] = cleaned_phone
        else:
            print("❌ Invalid phone format. Phone not updated.")

    email = input(f"Enter new email [{contacts[name]['email']}]: ").strip()
    if email:
        if validate_email(email):
            contacts[name]['email'] = email
        else:
            print("❌ Invalid email format. Email not updated.")

    contacts[name]['updated_at'] = datetime.now().isoformat()
    print(f"✅ Contact '{name}' updated successfully!")
    save_contacts(contacts)

def delete_contact(contacts):
    name = input("\nEnter the exact name of the contact to delete: ").strip()
    if name in contacts:
        confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").lower()
        if confirm == 'y':
            del contacts[name] # Removes the key-value pair from the dictionary
            print(f"✅ Contact '{name}' deleted!")
            save_contacts(contacts)
    else:
        print(f"❌ Contact '{name}' not found.")

def calculate_statistics(contacts):
    total = len(contacts)
    groups = {}
    
    # Count contacts per group using the .get() method
    for info in contacts.values():
        grp = info.get('group', 'Other')
        groups[grp] = groups.get(grp, 0) + 1
    
    print("\n" + "=" * 30)
    print("      CONTACT STATISTICS")
    print("=" * 30)
    print(f"Total Contacts: {total}")
    for grp, count in groups.items():
        print(f"- {grp}: {count}")

# ==========================================
# 4. PRESENTATION LAYER (User Interface)
# Responsible ONLY for printing to terminal and getting input
# ==========================================
def display_contact(name, info):
    """Helper function to format and print a single contact."""
    print("-" * 40)
    print(f"👤 Name:   {name}")
    print(f"📞 Phone:  {info['phone']}")
    if info.get('email'):
        print(f"📧 Email:  {info['email']}")
    print(f"👥 Group:  {info.get('group', 'Other')}")

def main():
    # Load data once when the program starts
    contacts = load_contacts()
    print(f"✅ Loaded {len(contacts)} contacts from file.")

    while True:
        print("\n" + "=" * 40)
        print("      CONTACT MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Add New Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. View All Contacts")
        print("6. View Statistics")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            add_contact(contacts)
            
        elif choice == '2':
            search_term = input("\nEnter name to search: ").strip()
            results = search_contacts(contacts, search_term)
            if not results:
                print(f"❌ No contacts found matching '{search_term}'.")
            else:
                print(f"\n🔍 Found {len(results)} matching contact(s):")
                for name, info in results.items():
                    display_contact(name, info)
                    
        elif choice == '3':
            update_contact(contacts)
            
        elif choice == '4':
            delete_contact(contacts)
            
        elif choice == '5':
            if not contacts:
                print("\n📭 Your contact book is empty.")
            else:
                print(f"\n--- ALL CONTACTS ({len(contacts)} total) ---")
                for name, info in contacts.items():
                    display_contact(name, info)
                    
        elif choice == '6':
            calculate_statistics(contacts)
            
        elif choice == '7':
            save_contacts(contacts) # Final save before exiting
            print("\n💾 Contacts saved. Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please select a number between 1 and 7.")

if __name__ == "__main__":
    main()