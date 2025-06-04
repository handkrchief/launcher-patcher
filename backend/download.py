import requests

def download_patch_file(url: str, save_path: str, update_progress: callable):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        if total_size == 0:
            raise Exception("Invalid or missing content-length. Cannot track download progress.")

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                update_progress(downloaded / total_size)
        
        update_progress(1.0)
