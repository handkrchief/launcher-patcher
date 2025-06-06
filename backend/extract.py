import time
import zipfile

def extract_patch_file(zip_path: str, extract_to: str, update_progress: callable):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        file_list = zf.namelist()
        total_files = len(file_list)

        # Extract each file and update progress     FIX ON UI (NOT WORKING)
        for i, file_name in enumerate(file_list):
            zf.extract(file_name, path=extract_to)
            update_progress((i + 1) / total_files)  # Report progress as a fraction
            time.sleep(0.001)  # Tiny delay for UI responsiveness