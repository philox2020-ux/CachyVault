import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Use the exact database storage file name we initialized earlier
DB_FILE = "vault_storage.json"

class CachyVaultGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🔐 CachyVault v1.0 - Private Password Locker")
        self.root.geometry("680x520")
        self.root.minsize(500, 400)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Application Form State Variables
        self.account_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self._ensure_database_exists()
        self._create_widgets()

    def _ensure_database_exists(self):
        """Ensures our JSON file is initialized on disk right on startup."""
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, "w") as f:
                json.dump({}, f)

    def _create_widgets(self):
        """Constructs and arranges all UI elements."""
        # Top Header Banner Frame
        header = ttk.Frame(self.root, padding="10 10 10 5")
        header.pack(fill=tk.X)
        ttk.Label(header, text="CachyVault Cryptographic Storage", font=("Helvetica", 14, "bold")).pack(anchor=tk.W)
        ttk.Label(header, text="Secure account profiling and instantaneous credential retrieval.", font=("Helvetica", 9, "italic"), foreground="#555555").pack(anchor=tk.W)

        # 📥 LEFT PANEL: Add New Password Profile Input Box Layout
        left_frame = ttk.LabelFrame(self.root, text="Add New Credentials", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(left_frame, text="Account Name (e.g. EpicGames):").pack(anchor=tk.W, pady=2)
        ttk.Entry(left_frame, textvariable=self.account_var).pack(fill=tk.X, pady=2)

        ttk.Label(left_frame, text="Username / Email:").pack(anchor=tk.W, pady=2)
        ttk.Entry(left_frame, textvariable=self.username_var).pack(fill=tk.X, pady=2)

        ttk.Label(left_frame, text="Secret Password:").pack(anchor=tk.W, pady=2)
        ttk.Entry(left_frame, textvariable=self.password_var, show="*").pack(fill=tk.X, pady=2) # Uses * mask to hide text input characters

        ttk.Button(left_frame, text="🔒 Save into Vault Locker", command=self.save_to_database).pack(fill=tk.X, pady=15)

        # 🔍 RIGHT PANEL: Password Search & Checking Room Layout
        right_frame = ttk.LabelFrame(self.root, text="Check Saved Passwords", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(right_frame, text="Search Account Profile Name:").pack(anchor=tk.W, pady=2)
        
        search_bar_frame = ttk.Frame(right_frame)
        search_bar_frame.pack(fill=tk.X, pady=2)
        
        ttk.Entry(search_bar_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(search_bar_frame, text="🔍 Check", command=self.retrieve_password).pack(side=tk.RIGHT)

        # Display screen text layout feed console area box
        ttk.Label(right_frame, text="Vault Retrieval Monitor Feed:").pack(anchor=tk.W, pady=(10, 2))
        self.display_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=12, font=("Consolas", 10), state=tk.DISABLED)
        self.display_area.pack(fill=tk.BOTH, expand=True)

    def save_to_database(self):
        """Saves target inputs into the JSON storage map layer."""
        account = self.account_var.get().strip()
        user = self.username_var.get().strip()
        pwd = self.password_var.get().strip()

        if not account or not user or not pwd:
            messagebox.showwarning("Validation Error", "All entry profiling fields are required!")
            return

        with open(DB_FILE, "r") as f:
            data_map = json.load(f)

        # Add the credentials variables map structure inside the storage index layout
        data_map[account.lower()] = {"display_name": account, "user": user, "pass": pwd}

        with open(DB_FILE, "w") as f:
            json.dump(data_map, f, indent=4)

        # Flash a true confirmation notice popup box onto your screen layout area canvas
        messagebox.showinfo("Success", f"Credentials for '{account}' saved successfully!")
        
        # Clear fields back to clear standby
        self.account_var.set("")
        self.username_var.set("")
        self.password_var.set("")

    def retrieve_password(self):
        """Searches the database and displays the credentials on your screen panel."""
        search_target = self.search_var.get().strip().lower()

        if not search_target:
            messagebox.showwarning("Input Error", "Please type an account name to check.")
            return

        with open(DB_FILE, "r") as f:
            data_map = json.load(f)

        self.display_area.config(state=tk.NORMAL)
        self.display_area.delete("1.0", tk.END)

        # 🕵️‍♂️ CHECK LOGIC: Look up the account inside our storage file index list variables
        if search_target in data_map:
            record = data_map[search_target]
            output_text = (
                f"📂 ACCOUNT ACCOUNT PROFILE MATCHED!\n"
                f"---------------------------------\n"
                f"🔹 Name:     {record['display_name']}\n"
                f"👤 Username: {record['user']}\n"
                f"🔑 Password: {record['pass']}\n"
                f"---------------------------------\n"
            )
            self.display_area.insert(tk.END, output_text)
        else:
            self.display_area.insert(tk.END, f"❌ ERROR: No account credentials found for match input target '{search_target}'.")

        self.display_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CachyVaultGUI(root)
    root.mainloop()
