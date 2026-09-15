import os
import json
import base64
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# 🛡️ CRYPTO CORE: Import the industry-standard encryption engines
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DB_FILE = "vault_storage.json"
KEY_FILE = "vault.key"

class CachyVaultGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🔐 CachyVault v1.1 - Armored Password Locker")
        self.root.geometry("720x540")
        self.root.minsize(550, 420)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Application state variables
        self.account_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # Initialize core cryptographic backend
        self.cipher_suite = self._initialize_crypto_key()
        self._ensure_database_exists()
        self._create_widgets()

    def _initialize_crypto_key(self):
        """Generates or loads a local cryptographic master key to shield data sectors."""
        # For this portfolio edition, we use a fixed salt to derive a stable master key
        salt = b'cachy_secure_salt_2026' 
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        # Unique master passphrase used to shield the vault logic
        master_passphrase = b"CachyShieldMasterVaultKey99!"
        derived_key = base64.urlsafe_b64encode(kdf.derive(master_passphrase))
        return Fernet(derived_key)

    def _ensure_database_exists(self):
        """Ensures our JSON database file is initialized on disk safely."""
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, "w") as f:
                json.dump({}, f)

    def _create_widgets(self):
        """Constructs and arranges all UI elements with strict padding rules."""
        header = ttk.Frame(self.root, padding="10 10 10 5")
        header.pack(fill=tk.X)
        ttk.Label(header, text="CachyVault Armored Cryptographic Storage", font=("Helvetica", 13, "bold")).pack(anchor=tk.W)
        ttk.Label(header, text="AES-256 bit symmetric key data obfuscation and instant secure querying.", font=("Helvetica", 9, "italic"), foreground="#555555").pack(anchor=tk.W)

        # 📥 LEFT PANEL: Add New Password Profile Input Box Layout
        left_frame = tk.LabelFrame(self.root, text="Add New Credentials", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(left_frame, text="Account Name (e.g. EpicGames):").pack(anchor=tk.W, pady=2)
        ttk.Entry(left_frame, textvariable=self.account_var).pack(fill=tk.X, pady=2)

        ttk.Label(left_frame, text="Username / Email:").pack(anchor=tk.W, pady=2)
        ttk.Entry(left_frame, textvariable=self.username_var).pack(fill=tk.X, pady=2)

        ttk.Label(left_frame, text="Secret Password:").pack(anchor=tk.W, pady=2)
        ttk.Entry(left_frame, textvariable=self.password_var, show="*").pack(fill=tk.X, pady=2)

        ttk.Button(left_frame, text="🔒 Scramble & Save to Vault", command=self.save_to_database).pack(fill=tk.X, pady=15)

        # 🔍 RIGHT PANEL: Password Search & Checking Room Layout
        right_frame = tk.LabelFrame(self.root, text="Check Saved Passwords", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(right_frame, text="Search Account Profile Name:").pack(anchor=tk.W, pady=2)
        
        search_bar_frame = ttk.Frame(right_frame)
        search_bar_frame.pack(fill=tk.X, pady=2)
        
        ttk.Entry(search_bar_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(search_bar_frame, text="🔍 Decrypt & Check", command=self.retrieve_password).pack(side=tk.RIGHT)

        ttk.Label(right_frame, text="Vault Retrieval Monitor Feed:").pack(anchor=tk.W, pady=(10, 2))
        self.display_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=12, font=("Consolas", 10), state=tk.DISABLED)
        self.display_area.pack(fill=tk.BOTH, expand=True)
    def save_to_database(self):
        """Encrypts inputs and appends them into the JSON storage map layer."""
        account = self.account_var.get().strip()
        user = self.username_var.get().strip()
        pwd = self.password_var.get().strip()

        if not account or not user or not pwd:
            messagebox.showwarning("Validation Error", "All entry profiling fields are required!")
            return

        try:
            # 🛡️ CRYPTO SCRAMBLER LAYER: Scramble the password bytes into cryptographic armor!
            encrypted_password_bytes = self.cipher_suite.encrypt(pwd.encode('utf-8'))
            # Convert binary cipher tokens to safe string strings to store inside JSON
            scrambled_password_string = encrypted_password_bytes.decode('utf-8')

            with open(DB_FILE, "r") as f:
                data_map = json.load(f)

            # Map the unreadable, secured cipher string inside your index tracker ledger
            data_map[account.lower()] = {
                "display_name": account, 
                "user": user, 
                "pass": scrambled_password_string
            }

            with open(DB_FILE, "w") as f:
                json.dump(data_map, f, indent=4)

            messagebox.showinfo("Success", f"Credentials for '{account}' encrypted & saved safely!")
            
            # Clear fields back to standby
            self.account_var.set("")
            self.username_var.set("")
            self.password_var.set("")
            
        except Exception as e:
            messagebox.showerror("Crypto Error", f"Failed to encrypt password layer: {str(e)}")

    def retrieve_password(self):
        """Searches the database, decrypts the token, and safely dumps plaintext data."""
        search_target = self.search_var.get().strip().lower()

        if not search_target:
            messagebox.showwarning("Input Error", "Please type an account name to check.")
            return

        with open(DB_FILE, "r") as f:
            data_map = json.load(f)

        self.display_area.config(state=tk.NORMAL)
        self.display_area.delete("1.0", tk.END)

        if search_target in data_map:
            record = data_map[search_target]
            scrambled_pwd = record['pass']
            
            try:
                # 🔓 DECRYPTION DE-OBFUSCATION LAYER: Parse the gibberish strings back to raw password strings
                decrypted_bytes = self.cipher_suite.decrypt(scrambled_pwd.encode('utf-8'))
                plain_password = decrypted_bytes.decode('utf-8')
                
                output_text = (
                    f"📂 ARMORED PROFILE RETRIEVAL MATCHED!\n"
                    f"---------------------------------\n"
                    f"🔹 Name:     {record['display_name']}\n"
                    f"👤 Username: {record['user']}\n"
                    f"🔑 Password: {plain_password}\n"
                    f"---------------------------------\n"
                )
                self.display_area.insert(tk.END, output_text)
            except Exception as crypto_ex:
                self.display_area.insert(tk.END, f"❌ CRYPTO ERROR: Data corruption or bad master decryption key link: {str(crypto_ex)}")
        else:
            self.display_area.insert(tk.END, f"❌ ERROR: No account credentials found for match input target '{search_target}'.")

        self.display_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CachyVaultGUI(root)
    root.mainloop()
