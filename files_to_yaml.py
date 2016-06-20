# coding=utf-8

import argparse
import os
import ruamel.yaml as yaml

__author__ = 'Gareth Coles'

# Define and parse our command-line arguments

DESC = "Traverses a tree of files and folders and adds them to a given " \
       "YAML-format file, for use with a package.yml. Supports relative " \
       "paths - If you want files to be prefixed with 'plugins/auth', " \
       "ensure that they're in that directory, move two levels up and call " \
       "this script with 'plugins/auth' as an argument.\n\nNote that this " \
       "will overwrite any pre-existing list of files."

p = argparse.ArgumentParser(description=DESC)

p.add_argument(
    "file", help="The YAML-format file to write to"
)
p.add_argument(
    "directory", help="Relative path to the base directory"
)

p.add_argument(
    "-i", "--ignore",
    help="File extension to ignore. May be used multiple times - "
         "Defaults to .md, .pyc and .pyo",
    action='append',
    metavar=("extension",)
)

args = p.parse_args()

filename = args.file
directory = args.directory
ignore = args.ignore

# Default ignore list

if not ignore:
    ignore = [".md", ".pyc", ".pyo"]


def is_allowed(fn):
    """Checks whether a file should be ignored by extension"""
    for item in ignore:
        if fn.endswith(item):
            return False
    return True


def slash_sort(fn):
    """Used to sort dir names by the number of slashes in them"""
    return fn.count("/")

# Check whether the supplied paths exist and are correct

if not os.path.exists(filename):
    print("Error: {} does not exist.".format(filename))
    exit(1)

if not os.path.isfile(filename):
    print("Error: {} is not a file.".format(filename))
    exit(1)

if not os.path.exists(directory):
    print("Error: {} does not exist.".format(directory))
    exit(1)

if not os.path.isdir(directory):
    print("Error: {} is not a file.".format(directory))
    exit(1)

# Read in the existing YAML data

data = {}

try:
    with open(filename, "r") as fh:
        data = yaml.round_trip_load(fh)
except Exception as e:
    print("Failed to load YAML-format file: {}".format(e))
    exit(1)

dirs_set = set()
files_set = set()

print("Ignoring extensions: {}".format(", ".join(sorted(ignore))))
print("Walking directory tree: {}".format(directory))

for root, dirs, files in os.walk(directory):
    # Walk the tree, sanitising and storing the dirs and files within

    root = root.replace("\\", "/")
    if root.endswith("/"):
        root = root[:-1]

    dirs_set.add(root)
    [dirs_set.add(root + "/" + d.replace("//", "/")) for d in dirs]
    [files_set.add(root + "/" + f.replace("//", "/")) for f in filter(
        is_allowed, files
    )]

print("Found {} directories containing {} files.".format(
    len(dirs_set), len(files_set)
))

# Next we need to order the dirs by the number of slashes in them, so the
# package manager creates them in the correct order

dir_ordering = {}

for x in dirs_set:
    if not x.endswith("/"):
        x += "/"
    num = slash_sort(x)

    if num not in dir_ordering:
        dir_ordering[num] = []
    dir_ordering[num].append(x)

# Finally, pretty things up

final_dirs = []
final_files = sorted(list(files_set))

for key in sorted(dir_ordering.keys()):
    final_dirs += sorted(dir_ordering[key])

final_list = final_dirs + sorted(final_files)

# Store our new list of files and write it to the yaml file

data["files"] = final_list

try:
    with open(filename, "w") as fh:
        yaml.round_trip_dump(data, fh, default_flow_style=False)
except Exception as e:
    print("Failed to dump YAML data: {}".format(e))
    exit(1)
