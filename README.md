# GitHub File Encryption and Management

This program allows you to securely encrypt or decrypt files and upload/download them to/from a GitHub repository using the GitHub REST API.

## Features
- **Encryption and Decryption**: Securely encrypt and decrypt files using the `Fernet` encryption scheme.
- **GitHub Integration**: Upload and fetch files from a specified GitHub repository.
- **Command-line Interface**: Simple CLI for easy usage.

---

## Requirements
- Python 3.7+
- `cryptography` library
- `requests` library

Install the required libraries using:
```bash
pip install -r requirements.txt
```

---

## Setup

### 1. Create a Secret Key
Generate a secret key for encryption and save it as `secret.key`:
```bash
python key.py
```

### 2. Configure GitHub API
Edit the `.env` file to set the following variables:
- `OWNER`: Your GitHub username.
- `REPO_NAME`: The repository name.
- `BRANCH`: The branch where files will be uploaded or fetched.
- `TOKEN`: Your GitHub personal access token (with `repo` scope).

---

## Usage

Run the program using the following commands:

### **1. Encrypt Files**
Encrypt all files in a source directory and save them to a target directory:
```bash
python main.py encrypt <source_directory> <target_directory>
```

Example:
```bash
python main.py encrypt my_files encrypted_files
```

### **2. Decrypt Files**
Decrypt all files in a source directory and save them to a target directory:
```bash
python main.py decrypt <source_directory> <target_directory>
```

Example:
```bash
python main.py decrypt encrypted_files decrypted_files
```

### **3. Upload Files to GitHub**
Upload all files from a local directory to the root of your GitHub repository:
```bash
python main.py upload <local_directory>
```

Example:
```bash
python main.py upload encrypted_files
```

### **4. Fetch Files from GitHub**
Fetch all files from the root of your GitHub repository and save them to a local directory:
```bash
python main.py fetch <local_directory>
```

Example:
```bash
python main.py fetch downloaded_files
```

---

## File Structure
The program is organized as follows:
```
.
├── main.py               # Entry point for the program
├── github.py             # Contains GitHub upload and fetch logic
├── encrypt.py            # Contains encryption logic
├── decrypt.py            # Contains decryption logic
├── secret.key            # Secret key for encryption/decryption
├── key.py                # Contains key generation logic
└── README.md             # Documentation
```

---

## Notes
- Ensure that the `secret.key` file is stored securely and not uploaded to GitHub.
- Only files in the root directory of the GitHub repository are fetched; subdirectories are not supported in the current implementation.
- Use a `.gitignore` file to prevent sensitive files like `secret.key` from being uploaded to GitHub.

---
