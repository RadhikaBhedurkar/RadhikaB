import json
import os
from typing import Dict, List, Optional

class ContactBook:
    def __init__(self, filename: str = "contacts.json"):  # Fixed: __init__ not _init_
        self.filename = filename
        self.contacts: Dict[str, Dict[str, str]] = {}
        self.load_contacts()
    
    def load_contacts(self) -> None:
        """Load contacts from JSON file if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.contacts = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                self.contacts = {}
    
    def save_contacts(self) -> None:
        """Save contacts to JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=2)
    
    def add_contact(self) -> None:
        """Add a new contact with validation."""
        print("\n=== ADD NEW CONTACT ===")
        
        name = input("Enter contact name: ").strip()
        if not name:
            print("ERROR: Name cannot be empty!")
            return
        
        if name.lower() in [k.lower() for k in self.contacts.keys()]:
            print(f"ERROR: Contact '{name}' already exists!")
            return
        
        phone = input("Enter phone number: ").strip()
        email = input("Enter email address: ").strip()
        address = input("Enter address: ").strip()
        
        # Basic validation
        if not phone:
            print("ERROR: Phone number is required!")
            return
        
        self.contacts[name] = {
            "phone": phone,
            "email": email,
            "address": address
        }
        
        self.save_contacts()
        print(f"SUCCESS: Contact '{name}' added successfully!")
    
    def view_contacts(self) -> None:
        """Display all contacts in a formatted list."""
        if not self.contacts:
            print("\nNo contacts found!")
            return
        
        print("\n=== CONTACT LIST ===")
        print(f"{'Name':<20} {'Phone':<15} {'Email':<25} {'Address':<30}")
        print("-" * 90)
        
        for name, details in sorted(self.contacts.items()):
            print(f"{name:<20} {details['phone']:<15} {details['email']:<25} {details['address']:<30}")
        
        print(f"\nTotal contacts: {len(self.contacts)}")
    
    def search_contact(self) -> None:
        """Search for contacts by name or phone number."""
        if not self.contacts:
            print("\nNo contacts to search!")
            return
        
        print("\n=== SEARCH CONTACT ===")
        query = input("Enter name or phone number to search: ").strip().lower()
        
        if not query:
            print("ERROR: Search query cannot be empty!")
            return
        
        matches = []
        for name, details in self.contacts.items():
            if (query in name.lower() or 
                query in details['phone'] or 
                query in details['email'].lower()):
                matches.append((name, details))
        
        if matches:
            print(f"\nFound {len(matches)} match(es):")
            print(f"{'Name':<20} {'Phone':<15} {'Email':<25} {'Address':<30}")
            print("-" * 90)
            
            for name, details in matches:
                print(f"{name:<20} {details['phone']:<15} {details['email']:<25} {details['address']:<30}")
        else:
            print("No contacts found matching your search!")
    
    def update_contact(self) -> None:
        """Update an existing contact's details."""
        if not self.contacts:
            print("\nNo contacts to update!")
            return
        
        print("\n=== UPDATE CONTACT ===")
        name = input("Enter the name of the contact to update: ").strip()
        
        # Find contact (case-insensitive)
        actual_name = None
        for contact_name in self.contacts.keys():
            if contact_name.lower() == name.lower():
                actual_name = contact_name
                break
        
        if not actual_name:
            print(f"ERROR: Contact '{name}' not found!")
            return
        
        print(f"\nCurrent details for '{actual_name}':")
        current = self.contacts[actual_name]
        print(f"Phone: {current['phone']}")
        print(f"Email: {current['email']}")
        print(f"Address: {current['address']}")
        
        print("\nEnter new details (press Enter to keep current value):")
        
        new_phone = input(f"Phone ({current['phone']}): ").strip()
        new_email = input(f"Email ({current['email']}): ").strip()
        new_address = input(f"Address ({current['address']}): ").strip()
        
        # Update only if new values provided
        if new_phone:
            current['phone'] = new_phone
        if new_email:
            current['email'] = new_email
        if new_address:
            current['address'] = new_address
        
        self.save_contacts()
        print(f"SUCCESS: Contact '{actual_name}' updated successfully!")
    
    def delete_contact(self) -> None:
        """Delete a contact after confirmation."""
        if not self.contacts:
            print("\nNo contacts to delete!")
            return
        
        print("\n=== DELETE CONTACT ===")
        name = input("Enter the name of the contact to delete: ").strip()
        
        # Find contact (case-insensitive)
        actual_name = None
        for contact_name in self.contacts.keys():
            if contact_name.lower() == name.lower():
                actual_name = contact_name
                break
        
        if not actual_name:
            print(f"ERROR: Contact '{name}' not found!")
            return
        
        # Show contact details and confirm deletion
        print(f"\nContact to delete:")
        details = self.contacts[actual_name]
        print(f"Name: {actual_name}")
        print(f"Phone: {details['phone']}")
        print(f"Email: {details['email']}")
        print(f"Address: {details['address']}")
        
        confirm = input(f"\nAre you sure you want to delete '{actual_name}'? (y/N): ").strip().lower()
        
        if confirm == 'y' or confirm == 'yes':
            del self.contacts[actual_name]
            self.save_contacts()
            print(f"SUCCESS: Contact '{actual_name}' deleted successfully!")
        else:
            print("Deletion cancelled.")
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*50)
        print("CONTACT BOOK MANAGER")
        print("="*50)
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        print("="*50)
    
    def run(self) -> None:
        """Main application loop."""
        print("Welcome to Contact Book Manager!")
        
        while True:
            self.display_menu()
            choice = input("Choose an option (1-6): ").strip()
            
            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.view_contacts()
            elif choice == '3':
                self.search_contact()
            elif choice == '4':
                self.update_contact()
            elif choice == '5':
                self.delete_contact()
            elif choice == '6':
                print("\nThank you for using Contact Book Manager!")
                print("All contacts have been saved automatically.")
                break
            else:
                print("ERROR: Invalid choice! Please select 1-6.")
            
            input("\nPress Enter to continue...")

def main():
    """Main function to run the Contact Book application."""
    contact_book = ContactBook()
    contact_book.run()

if __name__ == "__main__":
    main()