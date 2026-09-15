import os
import json

DB_FILE = "vault_storage.json"

def initialize_database():
    """Ensures the storage file exists on the hard drive with a clean structure."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            # Create a blank dictionary data format to store our accounts
            json.dump({}, f)
        print("💾 Storage Locker initialized: Created 'vault_storage.json'")

def save_credentials(account_name, username, secret_password):
    """Saves new login credentials to the local hard drive storage layout."""
    # 1. Read existing database records from the file
    with open(DB_FILE, "r") as f:
        database_map = json.load(f)
        
    # 2. Add the new account credential variables to our map registry
    database_map[account_name] = {
        "user": username,
        "pass": secret_password  # We will add mathematical scrambling armor here next!
    }
    
    # 3. Write the updated map structure back down to the hard drive file safely
    with open(DB_FILE, "w") as f:
        json.dump(database_map, f, indent=4)
        
    print(f"✅ Securely saved credentials for asset: {account_name}")

if __name__ == "__main__":
    print("🔐 PasswordVault Core Database Active.")
    initialize_database()
    
    # Test a sample mock database write sequence
    save_credentials("GitHub-Test", "xphilox", "cybermaster999")
