# Ultros-tools
Development/etc tools for use when working with Ultros

## files_to_yaml.py

This tool is designed to help you remember to add all the files you need for your
package.yml - so that the package manager doesn't mysteriously miss any files.
We feel that it's fairly self-explanatory:

```
$ python2 files_to_yaml.py -h
usage: files_to_yaml.py [-h] [-i extension] file directory

Traverses a tree of files and folders and adds them to a given YAML-format
file, for use with a package.yml. Supports relative paths - If you want files
to be prefixed with 'plugins/auth', ensure that they're in that directory,
move two levels up and call this script with 'plugins/auth' as an argument.
Note that this will overwrite any pre-existing list of files.

positional arguments:
  file                  The YAML-format file to write to
  directory             Relative path to the base directory

optional arguments:
  -h, --help            show this help message and exit
  -i extension, --ignore extension
                        File extension to ignore. May be used multiple times.
                        Defaults to .md, .pyc and .pyo when not specified.
```

Notes:

* This should work on both Python 2 and Python 3, but we only test on Python 2.
* This requires `ruamel.yaml`. There are no other dependencies.
* This will reformat your file, but does attempt to keep your comments intact.
