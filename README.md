# Contact Management System

## Project Description
A comprehensive contact management system built with Python using dictionaries and functions. This system allows users to manage their contacts with full CRUD operations, search functionality, and automatic data persistence using JSON files. Designed with SOLID principles in mind, separating data storage, validation, business logic, and UI.

## Setup Instructions
1. Ensure Python is installed on your machine.
2. Open your terminal or command prompt.
3. Navigate to the project folder: `cd week3-contact-manager`
4. Run the main application: `python contacts_manager.py`
5. Run the tests: `python test_contacts.py`

## Code Structure
- `contacts_manager.py`: The main script with separated layers (Data, Validation, CRUD, UI).
- `contacts_data.json`: The database file where dictionary items are serialized and saved.
- `test_contacts.py`: Unit tests validating the regex operations for emails and phone numbers.
- `README.md`: Project documentation and setup guide.
- `requirements.txt`: Project dependencies.
- `.gitignore`: Specifies intentionally untracked files (e.g., `__pycache__/`).

## Technical Details
- **Architecture:** Follows the Single Responsibility Principle (SRP). Divided into Data, Validation, Business Logic, and Presentation layers.
- **Data Structures:** Uses a main dictionary to map contact names to a nested dictionary containing their `phone`, `email`, `group`, and `updated_at` properties.
- **Data Persistence:** Uses the `json` library with context managers (`with open()`) to ensure safe reading and writing to `contacts_data.json`.
- **Validation:** Utilizes the `re` (Regex) module. `re.sub(r'\D', '', phone)` strips out special characters for phone numbers.
- **Search:** Iterates over the dictionary items and uses `in` combined with `.lower()` to allow partial, case-insensitive string matching.

## What I Learned
1. **Dictionaries:** How to build, traverse, and modify nested dictionaries.
2. **Regex (Regular Expressions):** How to sanitize inputs and validate complex string formats like emails.
3. **Data Persistence:** Moving from ephemeral memory (data lost when the program closes) to persistent storage using JSON.
4. **SOLID Principles:** Organizing code into dedicated functions rather than a single monolithic block.