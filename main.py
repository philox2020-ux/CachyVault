import os
import json
import base64

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DB_FILE = "vault_storage.json"

class CachyVaultApp(App):
    def build(self):
        self.title = "🔐 CachyVault Mobile"
        self.cipher_suite = self._initialize_crypto_key()
        self._ensure_database_exists()

        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        main_layout.add_widget(Label(text="CachyVault Armored Mobile Locker", font_size='18sp', bold=True, size_hint_y=None, height=40))

        main_layout.add_widget(Label(text="Account Name:", size_hint_y=None, height=20))
        self.account_input = TextInput(multiline=False, size_hint_y=None, height=40)
        main_layout.add_widget(self.account_input)

        main_layout.add_widget(Label(text="Username / Email:", size_hint_y=None, height=20))
        self.username_input = TextInput(multiline=False, size_hint_y=None, height=40)
        main_layout.add_widget(self.username_input)

        main_layout.add_widget(Label(text="Secret Password:", size_hint_y=None, height=20))
        self.password_input = TextInput(multiline=False, password=True, size_hint_y=None, height=40)
        main_layout.add_widget(self.password_input)

        save_btn = Button(text="🔒 Scramble & Save", size_hint_y=None, height=50, background_color=(0.06, 0.64, 0.5, 1))
        save_btn.bind(on_press=self.save_to_database)
        main_layout.add_widget(save_btn)

        main_layout.add_widget(Label(text="Search Account:", size_hint_y=None, height=20))
        self.search_input = TextInput(multiline=False, size_hint_y=None, height=40)
        main_layout.add_widget(self.search_input)

        check_btn = Button(text="🔍 Decrypt & Check", size_hint_y=None, height=50, background_color=(0.1, 0.5, 0.8, 1))
        check_btn.bind(on_press=self.retrieve_password)
        main_layout.add_widget(check_btn)

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.display_label = Label(text="Vault Ready...", font_size='14sp', size_hint_y=None)
        self.display_label.bind(texture_size=self.display_label.setter('size'))
        self.scroll_view.add_widget(self.display_label)
        main_layout.add_widget(self.scroll_view)

        return main_layout

    def _initialize_crypto_key(self):
        salt = b'cachy_secure_salt_2026' 
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        derived_key = base64.urlsafe_b64encode(kdf.derive(b"CachyShieldMasterVaultKey99!"))
        return Fernet(derived_key)

    def _ensure_database_exists(self):
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, "w") as f:
                json.dump({}, f)

    def save_to_database(self, instance):
        account = self.account_input.text.strip()
        user = self.username_input.text.strip()
        pwd = self.password_input.text.strip()

        if not account or not user or not pwd:
            self.display_label.text = "⚠️ Fields required!"
            return

        encrypted_pwd = self.cipher_suite.encrypt(pwd.encode('utf-8')).decode('utf-8')
        with open(DB_FILE, "r") as f:
            data_map = json.load(f)
        data_map[account.lower()] = {"display_name": account, "user": user, "pass": encrypted_pwd}
        with open(DB_FILE, "w") as f:
            json.dump(data_map, f, indent=4)

        self.display_label.text = f"✅ Encrypted & Saved: {account}"
        self.account_input.text = ""
        self.username_input.text = ""
        self.password_input.text = ""

    def retrieve_password(self, instance):
        target = self.search_input.text.strip().lower()
        if not target: return
        with open(DB_FILE, "r") as f:
            data_map = json.load(f)
        if target in data_map:
            record = data_map[target]
            try:
                plain_pwd = self.cipher_suite.decrypt(record['pass'].encode('utf-8')).decode('utf-8')
                self.display_label.text = f"📂 FOUND!\nName: {record['display_name']}\nUser: {record['user']}\nPass: {plain_pwd}"
            except Exception:
                self.display_label.text = "❌ Decryption error."
        else:
            self.display_label.text = f"❌ '{target}' not found."

if __name__ == "__main__":
    CachyVaultApp().run()
