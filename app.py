import os
import json
import base64
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DB_FILE = "vault_storage.json"

class CachyVaultGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🔐 CachyVault v1.1 - Armored Password Locker")
        self.root.geometry("720x540")
        self.root.minsize(550, 420)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.account_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.cipher_suite = self._initialize_crypto_key()
        self._ensure_database_exists()
        self._create_widgets()

    def _initialize_crypto_key(self):
        salt = b'cachy_secure_salt_2026' 
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        derived_key = base64.urlsafe_b64encode(kdf.derive(b"CachyShieldMasterVaultKey99!"))
        return Fernet(derived_key)

    def _ensure_database_exists(self):
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, "w") as f:
                json.dump({}, f)

    def _create_widgets(self):
        header = ttk.Frame(self.root, padding="10 10 10 5")
        header.pack(fill=tk.X)
        ttk.Label(header, text="CachyVault Armored Cryptographic Storage", font=("Helvetica", 13, "bold")).pack(anchor=tk.W)
        ttk.Label(header, text="AES-256 bit symmetric key data obfuscation and instant secure querying.", font=("Helvetica", 9, "italic"), foreground="#555555").pack(anchor=tk.W)

        left_frame = tk.LabelFrame(self.root, text="Add New Credentials", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(left_frame, text="Account Name (e.g. EpicGames):").pack(anchor=tk.W, pady=2)
        ttk.Entry(left_frame, textvariable=self.account_var).pack(fill=tk.X, pady=2)

        ttk.Label(left_frame, text="Username / Email:").pack(anchor=tk.W, pady=2)
        ttk.Entry(left_frame, textvariable=self.username_var).pack(fill=tk.X, pady=2)

        ttk.Label(left_frame, text="Secret Password:").pack(anchor=tk.W, pady=2)
        ttk.Entry(left_frame, textvariable=self.password_var, show="*").pack(fill=tk.X, pady=2)

        ttk.Button(left_frame, text="🔒 Scramble & Save to Vault", command=self.save_to_database).pack(fill=tk.X, pady=15)

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
        account = self.account_var.get().strip()
        user = self.username_var.get().strip()
        pwd = self.password_var.get().strip()

        if not account or not user or not pwd:
            messagebox.showwarning("Validation Error", "All fields are required!")
            return

        try:
            encrypted_pwd = self.cipher_suite.encrypt(pwd.encode('utf-8')).decode('utf-8')
            with open(DB_FILE, "r") as f:
                data_map = json.load(f)
            data_map[account.lower()] = {"display_name": account, "user": user, "pass": encrypted_pwd}
            with open(DB_FILE, "w") as f:
                json.dump(data_map, f, indent=4)
            messagebox.showinfo("Success", f"Credentials for '{account}' encrypted & saved safely!")
            self.account_var.set("")
            self.username_var.set("")
            self.password_var.set("")
        except Exception as e:
            messagebox.showerror("Crypto Error", f"Failed to encrypt: {str(e)}")

    def retrieve_password(self):
        search_target = self.search_var.get().strip().lower()
        if not search_target:
            return
        with open(DB_FILE, "r") as f:
            data_map = json.load(f)
        self.display_area.config(state=tk.NORMAL)
        self.display_area.delete("1.0", tk.END)
        if search_target in data_map:
            record = data_map[search_target]
            try:
                plain_password = self.cipher_suite.decrypt(record['pass'].encode('utf-8')).decode('utf-8')
                output_text = f"📂 PROFILE RETRIEVED!\n🔹 Name: {record['display_name']}\n👤 User: {record['user']}\n🔑 Pass: {plain_password}\n"
                self.display_area.insert(tk.END, output_text)
            except Exception as e:
                self.display_area.insert(tk.END, f"❌ Decryption Error: {str(e)}")
        else:
            self.display_area.insert(tk.END, f"❌ '{search_target}' not found.")
        self.display_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CachyVaultGUI(root)
    root.mainloop()
