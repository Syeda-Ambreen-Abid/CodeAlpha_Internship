# 📊 Stock Portfolio Tracker (Flask Web App)

A simple and elegant **Flask-based Stock Portfolio Tracker** that allows users to select stocks, enter quantities, view total investment, and save or reset their virtual portfolio — all through a clean and responsive web interface.

---

## 🚀 Features

- 📈 **Track multiple stocks** — add quantities for different companies  
- 💰 **View total investment value** in real time  
- 💾 **Download portfolio summary** as a text file (`portfolio.txt`)  
- 🔄 **Reset portfolio** anytime with a single click  
- 🌈 **Beautiful gradient design** with interactive UI (HTML + CSS inside Flask template)  

---

## 🧰 Technologies Used

| Component | Description |
|------------|-------------|
| **Python 3** | Core programming language |
| **Flask** | Web framework to serve the app |
| **HTML/CSS** | User interface (rendered via `render_template_string`) |
| **In-memory storage** | Stores user portfolio temporarily (resets when server restarts) |

