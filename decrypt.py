import os

def decrypt_file(file_path, target_dir, cipher):
    """Decrypt file content and name"""
    with open(file_path, "rb") as file:
        decrypted_data = cipher.decrypt(file.read())

    original_name = cipher.decrypt(os.path.basename(file_path).encode()).decode()
    os.makedirs(os.path.dirname(os.path.join(target_dir, original_name)), exist_ok=True)
    with open(os.path.join(target_dir, original_name), "wb") as file:
        file.write(decrypted_data)


def decrypt_directory(src_dir, target_dir, cipher):
    """Recursively decrypt all files in a directory"""
    for root, _, files in os.walk(src_dir):
        for file in files:
            decrypt_file(os.path.join(root, file), target_dir, cipher)
