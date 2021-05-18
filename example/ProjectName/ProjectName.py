import os
from Runtime import *

if __name__ == '__main__':
    project_path = os.path.split(os.path.realpath(__file__))[0]
    Entry.enter(Pack.pack(project_path))