import zipfile


def extract_patch_file(zip_path: str, extract_to: str, update_progress: callable):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        file_list = zf.namelist()
        total_files = len(file_list)

        for i, file_name in enumerate(file_list):
            zf.extract(file_name, path=extract_to)
            update_progress((i + 1) / total_files)