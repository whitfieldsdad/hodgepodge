# hodgepodge

> _A **hodgepodge** of hopefully helpful helper code_

![These are a few of my favourite functions](https://raw.githubusercontent.com/whitfieldsdad/images/main/a-few-of-my-favourite-things.jpg)

## Features

- Search for files;
- Pack files into archives;
- Perform pattern matching;
- Compress and decompress objects;
- Make the outputs from your tools more human-readable (e.g., by pretty-printing dates, file sizes, timestamps, and durations); and
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
$ python3 -m tox
...
Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
hodgepodge/__init__.py                             0      0   100%
hodgepodge/classes.py                             12      0   100%
hodgepodge/cli/__init__.py                         9      1    89%
...
hodgepodge/types.py                               86     46    47%
hodgepodge/uuid.py                                 3      0   100%
hodgepodge/ux.py                                  56      6    89%
------------------------------------------------------------------
TOTAL                                            730    199    73%
py3 run-test: commands[4] | /home/fishet/src/hodgepodge/.tox/py3/bin/python -m coverage html '--omit=.tox/*,tests/*'
_______________________________________ summary _______________________________________
  py3: commands succeeded
  congratulations :)
````

A code coverage report will automatically be written to: `htmlcov/index.html` whenever you run `tox`.

On Linux systems, you can use `xdg-open` to open the file using the system's default web browser:

```shell
$ xdg-open htmlcov/index.html
```
