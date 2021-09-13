# hodgepodge

> _A **hodgepodge** of hopefully helpful helper code_

![These are a few of my favourite functions](https://raw.githubusercontent.com/whitfieldsdad/images/main/a-few-of-my-favourite-things.jpg)

## Features

- Search for files and directories;
- Hash files;
- Pack files into ZIP archives;
- Perform pattern matching using regular expressions or UNIX-style glob patterns;
- Compress and decompress objects;
- Parse dates and times;
- Read STIX 2.0 objects from local files, directories, or TAXII servers 🚖🚦;
- Make the outputs from your tools more human-readable (e.g., by pretty-printing dates, file sizes, timestamps, and durations, joining lists with an Oxford comma); and
- ✨ _Way_, __*way*__, __way__ more ✨.

Supported hash algorithms:
- MD5
- SHA-1
- SHA-256
- SHA-512

Supported archive formats:
- ZIP

Supported compression algorithms:
- GZIP

## Installation

To install from source:

```shell
$ git clone git@github.com:whitfieldsdad/hodgepodge.git
$ python3 setup.py install
```

## Tests

You can run the unit tests and measure code coverage at the same time as follows:

```shell
$ make test
make test
poetry run coverage run -m pytest
================================= test session starts =================================
platform linux -- Python 3.8.10, pytest-5.4.3, py-1.10.0, pluggy-0.13.1
rootdir: /home/fishet/src/hodgepodge
collected 59 items

tests/test_classes.py ...                                                       [  5%]
tests/test_compression.py ..                                                    [  8%]
tests/test_files.py ............                                                [ 28%]
tests/test_hashing.py ..                                                        [ 32%]
tests/test_patterns.py .....                                                    [ 40%]
tests/test_platforms.py .                                                       [ 42%]
tests/test_stix2.py ......                                                      [ 52%]
tests/test_time.py ...                                                          [ 57%]
tests/test_type.py ......                                                       [ 67%]
tests/test_uuid.py .                                                            [ 69%]
tests/test_ux.py ........                                                       [ 83%]
tests/toolkits/host/file/test_search.py ..........                              [100%]

================================= 59 passed in 5.12s ==================================
````

A code coverage report will automatically be written to: `htmlcov/index.html` whenever you run `tox`.

On Linux systems, you can use `xdg-open` to open the file using the system's default web browser:

```shell
$ xdg-open htmlcov/index.html
```
