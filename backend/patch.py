import os
from backend.download import download_patch_file
from backend.extract import extract_patch_file
from backend.utils import extract_version_from_patch_name, get_launcher_root
from backend.version import fetch_remote_version, generate_patch_list, read_local_version, write_local_version

def run_patcher(base_url: str, version_file: str, temp_dir: str, update_progress: callable, update_status: callable):
    
    # Read local and remote versions
    local_version = read_local_version(version_file)
    remote_version = fetch_remote_version(base_url + "/version.dat")

    # Generate list of required patches
    patch_list = generate_patch_list(local_version, remote_version)
    os.makedirs(temp_dir, exist_ok=True)
    
    # If no patches needed, notify and exit
    if not patch_list:
        update_status("Game is up to date.")
        return True
    
    # Download and apply each patch in order
    for patch_name in patch_list:
        update_status(f"Downloading {patch_name}...")
        patch_url = base_url + f"/{patch_name}"
        save_path = os.path.join(temp_dir, patch_name)

        try:
            # Download patch file
            download_patch_file(patch_url, save_path, update_progress)

            # Extract patch contents
            update_status(f"Extracting {patch_name}...")
            extract_patch_file(save_path, get_launcher_root(), update_progress)

            # Update local version after successful extraction
            new_version = extract_version_from_patch_name(patch_name)
            write_local_version(version_file, new_version)

            # Remove patch file after extraction
            os.remove(save_path)
        except Exception as e:
            # On error, update status and stop patching
            update_status(f"Failed on {patch_name}: {e}")
            break
    
    return True