# 🚀 VibeDock

**VibeDock** is a desktop application launcher that lets you organize your favorite files, folders, and websites into named profiles. Launch everything you need with one click.

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

---

## ✨ Features

- **🔐 User Authentication** – Sign up, sign in, and delete accounts
- **📁 Profile Management** – Create, edit, and delete custom profiles
- **📎 Resource Types** – Add files, folders, or URLs to any profile
- **🖱️ Drag & Drop** – Drag files/folders directly into the app
- **⚡ Quick Access** – Recently used profiles appear on dashboard
- **🚀 One-Click Launch** – Launch all resources in a profile simultaneously
- **💾 JSON Storage** – All data saved locally in human-readable JSON
- **🪟 Cross-Platform** – Works on Windows, macOS, and Linux

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core programming language |
| **PyQt6** | GUI framework for windows, buttons, lists |
| **JSON** | Local data storage for users and profiles |
| **subprocess** | Launch external applications independently |
| **webbrowser** | Open URLs in default browser |
| **re (regex)** | Email format validation |

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/2012hhh2012/VibeDock.git
   cd VibeDock
   ```

2. **Install dependencies**
   ```bash
   pip install PyQt6
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

---

## 🎮 How to Use

### 1. Create an Account
- Click "Sign Up" on the login screen
- Enter username, email, and password (min. 6 characters)
- Your data is saved locally in `users-data.json`

### 2. Create a Profile
- Go to **Profiles** → **Add Profile**
- Enter a name (e.g., "Work", "Gaming", "Study")

### 3. Add Resources to a Profile
- Click **Edit** on any profile
- Add resources in three ways:
  - **Browse** – Select a file from your computer
  - **URL** – Type a website address
  - **Drag & Drop** – Drag files/folders directly into the list

### 4. Launch a Profile
- Select a profile from **Dashboard** or **Profiles**
- Click **Launch** – everything opens at once!

### 5. Quick Access
- Recently launched profiles automatically appear on the Dashboard
- Most recent profile appears at the top

---

## 📁 Project Structure

```
VibeDock/
├── main.py                 # Main application code
├── signin.ui               # Sign in window UI
├── signup.ui               # Sign up window UI
├── dashboard.ui            # Dashboard window UI
├── profiles.ui             # Profiles window UI
├── editprofile.ui          # Edit profile window UI
├── settings.ui             # Settings window UI
├── vibedockicon.png        # Application icon
├── users-data.json         # User data (created automatically)
└── README.md               # This file
```

---

## 🗂️ JSON Data Structure

```json
[
  {
    "username": "john",
    "password": "pass123",
    "email": "john@example.com",
    "profiles": {
      "Work": {
        "resources": ["C:\\Projects", "https://github.com"]
      }
    },
    "quickaccess": ["Work"]
  }
]
```

---

## 🖥️ Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Windows 10/11 | ✅ Fully supported | Native file explorer integration |
| macOS | ✅ Supported | Uses `open` command |
| Linux | ✅ Supported | Uses `xdg-open` command |

---

## 🔧 Building an Executable (Windows)

To create a standalone `.exe` file:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "signin.ui;." --add-data "signup.ui;." --add-data "dashboard.ui;." --add-data "profiles.ui;." --add-data "settings.ui;." --add-data "editprofile.ui;." --add-data "vibedockicon.png;." --icon="vibedockicon.png" --name="VibeDock" main.py
```

The executable will be in the `dist/` folder.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 Future Improvements

- [ ] Focus timer for productivity sessions
- [ ] Launch on system startup
- [ ] Minimize to system tray
- [ ] Export/Import profiles
- [ ] Search/filter resources
- [ ] Dark/light theme toggle
- [ ] Keyboard shortcuts

---

## 📄 License

This project is licensed under the MIT License - see below:

```
MIT License

Copyright (c) 2025 VibeDock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...

Full license text: https://opensource.org/licenses/MIT
```

---

## 👨‍💻 Author

**2012hhh2012**
- GitHub: [@2012hhh2012](https://github.com/2012hhh2012)

---

## ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

## 🙏 Acknowledgments

- PyQt6 team for the amazing GUI framework
- All contributors and testers

---

**Made with ❤️ for productivity**