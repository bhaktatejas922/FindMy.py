import PyInstaller.__main__
import sys
import os

if __name__ == "__main__":
    sys.setrecursionlimit(5000)

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set the path to local_run.py relative to the current script
    local_run_path = os.path.join(current_dir, 'local_run.py')
    
    # Determine the path to the findmy module
    findmy_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'FindMy.py')  # Two directories up
    print(findmy_path)
    PyInstaller.__main__.run([
        local_run_path,
        '--onefile',
        '--name=register_icloud',
        f'--add-data={findmy_path}:.',  # Add the FindMy.py file to the bundle
        '--hidden-import=findmy',
        '--hidden-import=requests',
        '--hidden-import=argparse',
        '--hidden-import=json',
        '--hidden-import=secrets',
        '--hidden-import=typing_extensions',
        '--hidden-import=srp',
        '--hidden-import=cryptography',
        '--hidden-import=beautifulsoup4',
        '--hidden-import=aiohttp',
        '--hidden-import=bleak',
        '--additional-hooks-dir=.',
    ])

# Create a new file named 'hook-typing_extensions.py' in the same directory as build.py
with open(os.path.join(current_dir, 'hook-typing_extensions.py'), 'w') as f:
    f.write("""
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('typing_extensions')
    """)