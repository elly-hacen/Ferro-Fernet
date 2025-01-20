import argparse
import os
from encrypt import encrypt_directory
from decrypt import decrypt_directory
from cryptography.fernet import Fernet
from github import upload_folder_to_github, fetch_files_from_github


def load_key():
    key_path = "secret.key"
    if not os.path.exists(key_path):
        print("Error: secret.key file not found.")
        exit(1)
    return Fernet(open(key_path, "rb").read())


def validate_directory(path, purpose="source"):
    if not os.path.exists(path):
        print(f"Error: {purpose.capitalize()} directory '{path}' does not exist.")
        exit(1)
    if not os.path.isdir(path):
        print(f"Error: {purpose.capitalize()} path '{path}' is not a directory.")
        exit(1)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Encrypt, decrypt, upload, or fetch files securely using a secret key and GitHub.\n\n"
            "Commands:\n"
            "  encrypt: Encrypt files.\n"
            "  decrypt: Decrypt files.\n"
            "  upload: Upload files to GitHub.\n"
            "  fetch: Fetch files from GitHub.\n\n"
            "Examples:\n"
            "  python main.py encrypt <src_dir> <target_dir>\n"
            "  python main.py decrypt <src_dir> <target_dir>\n"
            "  python main.py upload <local_folder>\n"
            "  python main.py fetch <target_folder>\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Encrypt command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt files.")
    encrypt_parser.add_argument("src_dir", help="Source directory to encrypt.")
    encrypt_parser.add_argument("target_dir", help="Target directory to save encrypted files.")

    # Decrypt command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt files.")
    decrypt_parser.add_argument("src_dir", help="Source directory containing encrypted files.")
    decrypt_parser.add_argument("target_dir", help="Target directory to save decrypted files.")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload files to GitHub.")
    upload_parser.add_argument("local_folder", help="Local folder to upload to GitHub.")

    # Fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch files from GitHub.")
    fetch_parser.add_argument("target_folder", help="Local folder to save fetched files.")

    # Parse arguments
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "encrypt":
        validate_directory(args.src_dir, "source")
        cipher = load_key()
        print("Starting encryption...")
        encrypt_directory(args.src_dir, args.target_dir, cipher)
        print("Encryption completed successfully.")

    elif args.command == "decrypt":
        validate_directory(args.src_dir, "source")
        cipher = load_key()
        print("Starting decryption...")
        decrypt_directory(args.src_dir, args.target_dir, cipher)
        print("Decryption completed successfully.")

    elif args.command == "upload":
        validate_directory(args.local_folder, "local")
        print("Uploading files to GitHub...")
        upload_folder_to_github(args.local_folder)
        print("Upload completed.")

    elif args.command == "fetch":
        print("Fetching files from GitHub...")
        fetch_files_from_github(args.target_folder)
        print("Fetch completed.")

if __name__ == "__main__":
    main()
