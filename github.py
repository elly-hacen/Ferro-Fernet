import os
import requests
import base64
import environ

env = environ.Env()
env.read_env()

OWNER = env.str("OWNER") # GitHub username
BRANCH = env.str("BRANCH")
REPO_NAME = env.str("REPO_NAME")
TOKEN = env.str("TOKEN")


HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def get_github_api_url(path=""):
    return f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/contents/{path}"


def upload_file_to_github(local_file_path, repo_file_name):
    try:
        # Read and encode file content
        with open(local_file_path, "rb") as file:
            file_content = file.read()

        encoded_content = base64.b64encode(file_content).decode()

        payload = {
            "message": "Initial commit",
            "content": encoded_content,
            "branch": BRANCH,
        }

        response = requests.put(get_github_api_url(repo_file_name), json=payload, headers=HEADERS)

        if response.status_code == 201:
            pass
        else:
            print(f"Failed to upload: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"Error uploading: {e}")


def upload_folder_to_github(local_folder):
    """Upload all files in a folder to GitHub"""
    for root, _, files in os.walk(local_folder):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            upload_file_to_github(local_file_path, file_name)



def fetch_files_from_github(dest_path):
    try:
        response = requests.get(get_github_api_url(), headers=HEADERS)

        if response.status_code == 200:
            files = response.json()
            os.makedirs(dest_path, exist_ok=True)

            for file in files:
                if file["type"] == "file":  # Process only files
                    file_name = file["name"]
                    download_url = file["download_url"]
                    fetch_and_save_file(download_url, file_name, dest_path)
        else:
            print(f"Failed to fetch files: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"Error fetching files: {e}")


def fetch_and_save_file(download_url, file_name, dest_path):
    """Download a single file from GitHub and save it locally"""
    try:
        response = requests.get(download_url, headers=HEADERS)

        if response.status_code == 200:
            file_path = os.path.join(dest_path, file_name)
            with open(file_path, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"Error downloading: {e}")
