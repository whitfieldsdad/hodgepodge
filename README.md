# hodgepodge  

[![](https://img.shields.io/pypi/pyversions/hodgepodge)](https://pypi.org/project/hodgepodge/) [![](https://img.shields.io/pypi/wheel/hodgepodge)](https://pypi.org/project/hodgepodge/#files) [![](https://img.shields.io/pypi/l/hodgepodge)](https://github.com/whitfieldsdad/hodgepodge/blob/main/LICENSE.md)

> _A **hodgepodge** of hopefully helpful helper code_

![These are a few of my favourite functions](https://raw.githubusercontent.com/whitfieldsdad/images/main/a-few-of-my-favourite-things.jpg)

## FAQ

### What can it do?

- Search for files and directories;
- Hash files;
- Pack files into archives;
- Perform pattern matching;
- Compress and decompress objects;
- Parse dates and times;
- Read STIX 2.0 objects from local files, directories, or TAXII servers;
- Make the outputs from your tools more human-readable; and
- ✨ More ✨.

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

To install `hodgepodge` using `pip`:

```shell
$ pip install hodgepodge
```

To install `hodgepodge` from source (requires [`poetry`](https://github.com/python-poetry/poetry)):

```shell
$ git clone git@github.com:whitfieldsdad/hodgepodge.git
$ cd hodgepodge
$ make install
```

To install `hodgepodge` from source using `setup.py` (i.e. if you're not using `poetry`):

```shell
$ git clone git@github.com:whitfieldsdad/hodgepodge.git
$ cd hodgepodge
$ python3 setup.py install
```

## Testing

You can run the unit tests for this package as follows:

```shell
$ make test
```

A code coverage report will automatically be written to: `htmlcov/index.html`.

On Linux systems, you can use `xdg-open` to open this file using the system's default web browser:

```shell
$ xdg-open htmlcov/index.html
```
