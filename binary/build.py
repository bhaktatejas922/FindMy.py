import PyInstaller.__main__
import sys
import os

if __name__ == "__main__":
    sys.setrecursionlimit(5000)  # Increase recursion limit to handle complex imports

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set the path to local_run.py relative to the current script
    local_run_path = os.path.join(current_dir, 'local_run.py')

    PyInstaller.__main__.run([
        local_run_path,
        '--onefile',
        '--name=register_icloud',
        # '--add-data=FindMy.py:FindMy',
        '--hidden-import=findmy',
        '--hidden-import=requests',
        '--hidden-import=argparse',
        '--hidden-import=json',
    ])