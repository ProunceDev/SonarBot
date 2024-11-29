import os, glob
from interactions import *

ext_filenames = glob.glob(os.path.join("Extensions", "**", "*.py"), recursive=True)
EXTENSIONS = [os.path.splitext(filename)[0].replace(os.path.sep, ".") for filename in ext_filenames]