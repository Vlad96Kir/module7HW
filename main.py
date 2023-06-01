import os
import glob
import shutil


def normalize(name):
    invalid_chars = r'<>:"/\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    name = name.strip()
    return name


# Створення папки clean_folder
os.mkdir('clean_folder')

# Зміна поточної робочої директорії на папку clean_folder
os.chdir('clean_folder')

# Створення папки-модуля clean_folder
os.mkdir('clean_folder')

# Створення файлу clean.py
with open('clean_folder/clean.py', 'w') as file:
    file.write('''
import os
import glob
import shutil


def normalize(name):
    invalid_chars = r'<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    name = name.strip()
    return name


extensions = {
    "jpg": "images",
    "jpeg": "images",
    "png": "images",
    "svg": "images",
    "pdf": "documents",
    "xlsx": "documents",
    "doc": "documents",
    "docx": "documents",
    "txt": "documents",
    "pptx": "documents",
    "mp3": "audio",
    "wav": "audio",
    "ogg": "audio",
    "amr": "audio",
    "mp4": "video",
    "avi": "video",
    "mov": "video",
    "mkv": "video",
    "zip": "archives",
    "gz": "archives",
    "tar": "archives",
}

path = ""

# Ignore these directories
ignored_dirs = {"archives", "video", "audio", "documents", "images"}

for extension, folder_name in extensions.items():
    files = glob.glob(os.path.join(path, f"*.{extension}"))
    print(f"[*] Found {len(files)} file(s) with extension '{extension}'.")

    if not os.path.isdir(os.path.join(path, folder_name)) and files:
        os.mkdir(os.path.join(path, folder_name))
        print(f"[+] Created folder '{folder_name}'.")

    for file in files:
        basename = os.path.basename(file)
        dst = os.path.join(path, folder_name, basename)

        if folder_name == "archives":
            archive_name = os.path.splitext(basename)[0]
            archive_dst = os.path.join(path, folder_name, normalize(archive_name))

            if not os.path.isdir(archive_dst):
                os.mkdir(archive_dst)
                print(f"[+] Created folder '{normalize(archive_name)}' inside 'archives'.")

            print(f"[*] Extracting '{basename}' to '{archive_dst}'.")
            shutil.unpack_archive(file, archive_dst)
            os.remove(file)
            print(f"[-] Removed archive file '{basename}'.")

        elif folder_name not in ignored_dirs:
            print(f"[*] Moving file '{basename}' to '{dst}'.")
            shutil.move(file, dst)

# Remove empty directories
for root, dirs, _ in os.walk(path, topdown=False):
    for dir_name in dirs:
        folder_path = os.path.join(root, dir_name)
        if not os.listdir(folder_path):
            os.rmdir(folder_path)
            print(f"[-] Removed empty folder '{folder_path}'.")
''')

# Створення порожнього файлу __init__.py
open('clean_folder/__init__.py', 'w').close()

# Створення файлу setup.py
with open('setup.py', 'w') as file:
    file.write('''
from setuptools import setup

setup(
    name='clean_folder',
    version='1.0',
    packages=['clean_folder'],
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main'
        ]
    }
)
''')

