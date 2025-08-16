# BreachChecker

A **Cyber Threat Intelligence** command-line tool for scanning and analyzing data breaches, exposed emails, passwords, and domains via public APIs.

---

## Table of Contents

- [Features](#features)  
- [Use Cases](#use-cases)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Configuration & API Endpoints](#configuration--api-endpoints)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- **Email Breach Scanner**  
  Query the XposedOrNot breach database to identify breaches associated with an email address. Outputs a formatted table of breach names and statuses.

- **Breach Analytics Engine**  
  Deep-scan an email to retrieve a risk score (0–100), a risk label (Low/Medium/High), industry exposure breakdown, and password strength profile (plaintext leaks, easy-to-crack hashes, strong hashes, unknown).

- **Password Exposure Scanner**  
  Compute a SHA3-512 hash prefix of any password and anonymously check if it appears in known breaches. Reports occurrence count and password composition statistics.

- **Domain Breach Lister**  
  Fetch and display a list of breached domains and exposed record counts (shows top 25 by default).

- **Browse All Breaches**  
  Interactively list all recorded breaches (optionally filtered by domain), including breach ID, domain name, and breach date.

- **Automated Dependency Management**  
  Verifies Python ≥ 3.6 and pip availability. Automatically installs or upgrades required packages: `requests`, `tabulate`, and `colorama`. Provides colorized, animated CLI output.

---

## Use Cases

1. **Security Research**  
   Rapidly enumerate breach data for target email addresses, domains, or passwords.

2. **Incident Response**  
   Assess the scope and risk level of credential compromise following a suspected breach.

3. **Compliance Auditing**  
   Verify that organizational emails and domains are free from known breaches.

4. **Password Hygiene Checks**  
   Proactively test corporate or personal passwords against breach databases to enforce strong credential policies.

---

## Prerequisites

- Python 3.6 or higher  
- Git (optional, for cloning the repository)  
- Internet connection (public API access)

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/<your-username>/BreachChecker.git
   cd BreachChecker
   ```

2. **Make the script executable**  
   ```bash
   chmod +x breachchecker.py
   ```

3. **Run the script**  
   ```bash
   ./breachchecker.py
   ```
   The script will automatically verify your Python environment and install any missing dependencies.

---

## Usage

Upon running `breachchecker.py`, select an option from the interactive menu:

```text
1. 🔍 Check Email Breaches
2. 📊 Breach Analytics
3. 🔐 Check Password Exposure
4. 🌐 List Domain Breaches
5. 📋 Browse All Breaches
0. 🚪 Exit Console
```

- **Scan an email for breaches**  
  Select `1`, then enter the target email address.

- **Get breach risk analytics**  
  Select `2`, then enter the target email address.

- **Check password exposure**  
  Select `3`, then enter the target password.

- **List domain breaches**  
  Select `4` to retrieve the top 25 breached domains.

- **Browse all breaches**  
  Select `5` and optionally enter a domain filter.

---

## Configuration & API Endpoints

- **Base breach API**:  
  `https://api.xposedornot.com/v1`

- **Anonymous password API**:  
  `https://passwords.xposedornot.com/v1`

No API keys or authentication required; all data is publicly accessible.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.  
2. Create a feature branch (`git checkout -b feature/my-feature`).  
3. Commit your changes (`git commit -m "Add new feature"`).  
4. Push to the branch (`git push origin feature/my-feature`).  
5. Open a pull request describing your changes.

Please report issues or suggest enhancements via GitHub Issues.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
