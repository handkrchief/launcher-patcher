import requests
from constants import PATCH_PREFIX, PATCH_SUFFIX
from backend.utils import get_launcher_root

# Loads and reads a version file and returns the current version as an integer.
def read_local_version(path: str):
    try:
        with open(path, 'r') as file:
            content = file.readline().strip()
            return int(content)
    # treats missing version file as a first install
    except FileNotFoundError:
        print(f"File not found: {path}")
        return 0
    except ValueError:
        raise Exception(f"Error: Invalid integer format in file: {path}")

# Fetches the current version of the game from the remote server.
def fetch_remote_version(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response_content = response.text.strip()
        return int(response_content)
    except requests.exceptions.RequestException as e:
        raise Exception("Unable to fetch version. Please check your internet connection.")
    except ValueError:
        raise Exception("Error: Invalid version format received from server.")
    
# Generates a list of file names that are needed to download to be up to date.
def generate_patch_list(local_version: int, remote_version: int):
    patch_list = []

    if remote_version == local_version:
        return patch_list
    elif remote_version < local_version:
        raise Exception("Version is ahead of the latest release. Please delete version.dat and relaunch.")
    else:
        for i in range(local_version + 1, remote_version + 1):
            patch_list.append(PATCH_PREFIX + str(i) + PATCH_SUFFIX)

    return patch_list

def write_local_version(path: str, version: int):
    with open(path, "w") as file:
        file.write(str(version))

    