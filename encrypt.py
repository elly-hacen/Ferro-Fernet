import os
import subprocess

def encrypt_file(file_path, target_dir, cipher):
    """Encrypt file content and name"""
    with open(file_path, 'rb') as file:
        encrypted_data = cipher.encrypt(file.read())

    encrypted_name = cipher.encrypt(file_path.encode()).decode()
    os.makedirs(os.path.dirname(os.path.join(target_dir, encrypted_name)), exist_ok=True)

    with open(os.path.join(target_dir, encrypted_name), "wb") as file:
        file.write(encrypted_data)

    # Securely delete the original file
    secure_delete_file(file_path)


def encrypt_directory(src_dir, target_dir, cipher):
    """Recursively encrypt all files in a directory and remove directories"""
    for root, _, files in os.walk(src_dir, topdown=False):
        for file in files:
            encrypt_file(os.path.join(root, file), target_dir, cipher)

        try:
            os.rmdir(root)
        except OSError:
            pass


def secure_delete_file(file_path):
    """Securely delete a file using shred with 30 passes"""
    try:
        subprocess.run(["shred", '-u', '-n', '30', file_path], check=True)
    except subprocess.CalledProcessError as e:
         print(f"Error shredding file {file_path}: {e}")
