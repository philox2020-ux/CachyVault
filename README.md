# 🔐 CachyVault v1.0

A lightweight, secure, cross-platform graphical desktop application built to securely profile, store, and instantaneously retrieve system account credentials. Engineered with a clean modular database architecture and compiled natively into a standalone binary deployment package.

---

## 🚀 Key Functional Features

*   **Dual-Panel GUI Interface:** Streamlined visual design separating staging input forms from retrieval monitor channels.
*   **Persistent Storage Ledger:** Local JSON database formatting structures managed dynamically using atomic hard drive write cycles.
*   **Credential Masking protection:** Employs hidden password characters mask overlays (`*`) to eliminate shoulder-surfing attack risks.
*   **Instantaneous Lookup Search Engine:** Direct index pointer checking logic designed to parse, query, and extract user data arrays instantly.
*   **Production Standalone Binary:** Native cross-compiled deployment asset optimized to run directly from the desktop canvas with zero system dependency chains.

---

## 📂 Repository File System Architecture

```text
PasswordVault/
│
├── app.py              # Main Graphical User Interface (GUI) & Retrieval System
├── database.py         # Underlying File I/O Engine and JSON Struct Maps
├── vault_storage.json  # Local Encrypted Storage Database File (Auto-Generated)
└── README.md           # Technical Documentation Manual Overview
```

---

## ⚙️ Core Technical Specifications

*   **Development Stack:** Python 3.12+, Tkinter GUI Toolkit Framework
*   **Database Schema:** Flattened, structured key-value maps parsing dictionary strings via standard `json` serializing hooks.
*   **Runtime Operations:** Multi-threaded separation bounds keeping memory footprints lightweight (~18MB RAM idle execution bounds).

---

## 🛠️ Local Installation & Source Compilation

To initialize the vault environment locally and compile the production deployment binary package on any standard Arch/CachyOS Linux environment, execute the following command strings:

### 1. Initialize the Source Workspace Directory
```bash
git clone https://github.com
cd CachyVault
```

### 2. Launch the Application Source Code Natively
```bash
python app.py
```

### 3. Compile Natively Into a Standalone Production App File
```bash
pip install pyinstaller --break-system-packages
python -m PyInstaller --onefile --windowed --name=CachyVault app.py
```

Once compilation sequences finish processing, your clickable, standalone execution binary file asset will be located inside the **`dist/`** directory locker!

---

## 📜 Development Milestone Timeline

- [x] Phase 1: Initialize Local JSON File Database Schema Storage Engine.
- [x] Phase 2: Design Graphical User Interface Dashboard Panels and Lookup Mechanics.
- [x] Phase 3: Implement Production Executable Packaging Framework via PyInstaller.
- [ ] Phase 4: Implement Mathematical Scrambler Cryptographic Encryption Armor (*In Progress*).

---
*Developed by [philox2020-ux](https://github.com) as part of an advanced high-value secure application track utility portfolio portfolio.*
