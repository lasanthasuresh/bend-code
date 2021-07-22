import os
from distutils.dir_util import copy_tree

def do_main():
    root_path = "D:\MSC-Project\company-data"
    destination_path =
    folders = os.listdir(root_path)
    for folder in folders:
        folder_path = os.path.join(root, folder)

    print(folders)





if __name__ == "__main__":
    do_main()