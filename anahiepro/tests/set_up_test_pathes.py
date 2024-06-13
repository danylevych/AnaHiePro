import sys
import os

current_file_path = os.path.abspath(__file__)
tests_dir = os.path.dirname(current_file_path)
module_dir = os.path.dirname(tests_dir)
project_root = os.path.dirname(module_dir)
sys.path.append(project_root)