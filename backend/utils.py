import os
import re
import sys

def get_launcher_root():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def extract_version_from_patch_name(patch_name: str):
    match = re.search(r'_(\d+)\.zip$', patch_name)
    if match:
        return int(match.group(1))
    raise ValueError(f"Could not extract version from: {patch_name}")

