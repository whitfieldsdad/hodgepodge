# `hodgepodge`

`hodgepodge` is a Python 3 library that provides a wide variety of functions and classes that I use in my own projects.

## Warnings

- This library is under active development.
- The API isn't stable and may change at any time without notice.

## Features

- Search for files and directories
- Hash files using one or more hashing algorithms<sub>1</sub>
- Read/write `polars.DataFrame` objects from/to CSV, JSON, JSONL, Parquet, and YAML files<sub>2</sub>
- Generate JSON Schemas from dictionaries or JSON, JSONL, YAML, Parquet, and CSV files
- Interpret JSON Schemas as directed acyclic graphs using NetworkX<sub>3</sub>
- Expand STIX 2 bundles into directories containing one STIX 2 bundle per object and one STIX 2 object per object type<sub>4</sub>
- Parse dates and times

<sub>1. Files are hashed with MD5, SHA-1, SHA-256, BLAKE2s, and BLAKE2b by default.</sub>

<sub>2. CSV, JSON, JSONL, and YAML files can optionally be compressed with GZIP.</sub>

<sub>3. Interpreting JSON Schemas as directed acyclic graphs allows us to abstractly analyze and visualize the structure of a given input file (e.g. a JSON file containing a response from a REST API).</sub>

<sub>4. By expanding STIX 2 bundles into files partitioned by object type we can easily determine which fields are available for different types of objects.</sub>

## Usage

### Python API

#### Reading and writing `polars.DataFrame` objects

`polars` provides a fast and efficient DataFrame implementation for Python. 

The `hodgepodge.dataframes` module provides functions to read and write `polars.DataFrame` objects from/to various file formats.

To write a `polars.DataFrame` to a file:

```python
from hodgepodge import dataframes

import polars as pl

hosts = [
    {'ip_address': '192.168.1.1', 'hostname': 'a'},
    {'ip_address': '192.168.1.2', 'hostname': 'b'},
    {'ip_address': '192.168.1.3', 'hostname': 'c'},
]
df = pl.DataFrame(hosts)

dataframes.write_dataframe(df, 'example.json')
dataframes.write_dataframe(df, 'example.jsonl')
dataframes.write_dataframe(df, 'example.jsonl.gz')
dataframes.write_dataframe(df, 'example.yaml')
dataframes.write_dataframe(df, 'example.parquet')
```

```bash
$ zcat example.jsonl.gz | jq --slurp
```

```json
[
  {
    "ip_address": "192.168.1.1",
    "hostname": "a"
  },
  {
    "ip_address": "192.168.1.2",
    "hostname": "b"
  },
  {
    "ip_address": "192.168.1.3",
    "hostname": "c"
  }
]
```

To read a `polars.DataFrame` from a file:

```python
from hodgepodge import dataframes

df = dataframes.read_dataframe('example.json')
df = dataframes.read_dataframe('example.jsonl')
df = dataframes.read_dataframe('example.jsonl.gz')
df = dataframes.read_dataframe('example.yaml')
df = dataframes.read_dataframe('example.parquet')
```