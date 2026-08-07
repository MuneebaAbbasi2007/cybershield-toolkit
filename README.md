# 🛡️ CyberShield Toolkit

An AI-powered Cybersecurity Toolkit developed using Flask that combines multiple cybersecurity tools into one easy-to-use web application.

It helps users perform network scanning, domain analysis, password security evaluation, DNS lookup, hash generation, AI-powered risk analysis, and PDF report generation from a single dashboard.
---

## 🚀 Features

- 🔐 Login Authentication
- 🔑 Password Strength Analyzer
- 🔒 Hash Generator (MD5, SHA-1, SHA-256)
- 🌐 WHOIS Lookup
- 📡 DNS Lookup
- 🛰️ Network Scanner (Nmap)
- 🤖 AI-Powered Risk Analysis
- 📄 PDF Report Generation
- 🗂 SQLite Scan History
- ⚠️ Friendly Error Handling
---

## 🛠 Technologies Used

- Python
- Flask
- HTML5
- CSS3
- Bootstrap 5
- SQLite
- Nmap
- Python-WHOIS
- dnspython
- zxcvbn
- ReportLab
- Groq API
---

## 📂 Project Structure

```text
cybershield-toolkit/
│
├── app.py
├── modules/
├── templates/
├── static/
├── README.md
├── requirements.txt
└── .gitignore
```---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MuneebaAbbasi2007/cybershield-toolkit.git
```

### 2. Navigate to the Project Folder

```bash
cd cybershield-toolkit
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
---

## 👨‍💻 Developer

**Muneeba Abbasi**

Computer Science Student | Cybersecurity Enthusiast

This project was developed as part of my Cybersecurity Internship to integrate multiple security tools into a single web-based application.
---

## 📌 Project Purpose

CyberShield Toolkit is a web-based cybersecurity application developed to simplify common security assessment tasks. It combines multiple open-source security tools with AI-powered risk analysis, enabling users to perform security checks, understand the results, and generate professional PDF reports through a simple and user-friendly interface.

---

⭐ If you found this project useful, consider giving it a star on GitHub.
## Usage

1. Login with your credentials
2. Choose a tool from the dashboard: Hash Generator, Password Checker, WHOIS Lookup, DNS Lookup, or Network Scanner
3. Enter the required input and submit
4. View AI-powered risk analysis for each result
5. Download individual or combined PDF reports from the Dashboard

## Environment Variables

Create a `.env` file in the root directory with:

GROQ_API_KEY=your_groq_api_key
APP_USERNAME=your_username
APP_PASSWORD=your_password


## Note

The Network Scanner module requires Nmap to be installed on the host system. Some free hosting platforms may have restrictions on network scanning capabilities.