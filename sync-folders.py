#!/usr/bin/env python3
# sync-folders.py

from datetime import datetime, date, time
import os
from shutil import copyfile
import sys
# DEBUG
# import pdb

def usage():
    print("\tsync-folders.py usage:\n\t$sync-folders.py [command] [source folder] [target folder]\n\n\tCommands:\n- scan: Will scan through the specified folders and return the number of files already exiting at the target, the number of files to be copied and their size in bytes.\n- run: This will copy all files from the source folder and its subfolders to the target folder with the same folder structure. Duplicates (already existing at the target) will be skipped.")#

def scan_recursive(source_folder, target_folder):
    copy_file_counter = 0
    skip_file_counter = 0
    file_size = 0
    # Traverse through source folder structure / tree
    for path, subdirs, files in os.walk(source_folder):
        # For each file name found at the relevant level or node of the tree
        for name in files:
            # Construct target file path according to source file path in the tree
            source_file_path = os.path.join(path, name)
            target_file_path = source_file_path.replace(source_folder, target_folder)
            # Either increase copy or skip counter, when already existing
            if not os.path.isfile(target_file_path):
                file_size += os.path.getsize(source_file_path)
                copy_file_counter += 1
            else:
                skip_file_counter += 1

    print("Files existing: {0}\nFiles to copy: {1} ({2} Bytes)".format(skip_file_counter, copy_file_counter, file_size))


def copy_recursive(source_folder, target_folder):
    copy_file_counter = 0
    skip_file_counter = 0
    # Traverse through source folder structure / tree
    for path, subdirs, files in os.walk(source_folder):
        # For each file name found at the relevant level or node of the tree
        for subdir in subdirs:
            # Ensure all required folders are existing in the target folder structure
            target_path = path.replace(source_folder, target_folder)
            target_subdir = os.path.join(target_path, subdir)
            if not os.path.isdir(target_subdir):
                print("Creating target sub folder '{0}'".format(target_subdir))
                os.mkdir(target_subdir)
        for name in files:
            # Construct target file path according to source file path in the tree
            source_file_path = os.path.join(path, name)
            target_file_path = source_file_path.replace(source_folder, target_folder)
            # Either copy or skip, when already existing
            if not os.path.isfile(target_file_path):
                print("Copying '{0}' to '{1}'".format(source_file_path, target_file_path))
                copyfile(source_file_path, target_file_path)
                copy_file_counter += 1
            else:
                skip_file_counter += 1

    print("Copied {0} files. Skipped {1} files. Done.".format(copy_file_counter, skip_file_counter))

# Validate arguments
if len(sys.argv) != 4:
    usage()
    exit()

command = sys.argv[1]
source_folder = sys.argv[2]
target_folder = sys.argv[3]

print("Source folder is '{0}'. Target folder is '{1}'.".format(source_folder, target_folder))

if command == 'scan':
    scan_recursive(source_folder, target_folder)
elif command == 'copy':
    copy_recursive(source_folder, target_folder)
else:
    usage()