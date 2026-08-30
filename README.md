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

<sub>3. Interpreting JSON Schemas as directed acyclic graphs allows us to abstractly analyze and visualize the structure of any file that can be interpreted as JSON (e.g. a JSON file containing a response from a REST API, or a Parquet file containing tabular data).</sub>

<sub>4. By expanding STIX 2 bundles into files partitioned by object type we can easily determine which fields are available for different types of objects (e.g. the fields available for `x-mitre-tactic` objects from the MITRE ATT&CK framework).</sub>

## Usage

### Python API

- [Searching for files and directories](#searching-for-files-and-directories)
- [Getting file metadata](#getting-file-metadata)
- [Hashing files](#hashing-files)
- [Hashing byte strings](#hashing-byte-strings)
- [Reading and writing `polars.DataFrame` objects](#reading-and-writing-polarsdataframe-objects)
- [Converting JSON files into Parquet files](#converting-json-files-into-parquet-files)

#### Searching for files and directories

To search for files (e.g. files named `osquery*` within `/usr/bin`):

```python
import hodgepodge.files

paths = hodgepodge.files.iter_file_paths(
    roots=['/usr/bin'],
    filename_patterns=['osquery*'],
    include_files=True, 
    include_directories=False,
)
for path in paths:
    print(path)
```

```
/usr/bin/osqueryctl
/usr/bin/osqueryd
/usr/bin/osqueryi
```

To search for directories (e.g. directories named `osquery*` within `/`):

```python
import hodgepodge.files

paths = hodgepodge.files.iter_file_paths(
    roots=['/'],
    filename_patterns=['osquery*'],
    include_files=False, 
    include_directories=True,
)
for path in paths:
    print(path)
```

```
/etc/osquery
/opt/osquery
/opt/osquery/share/osquery
/var/osquery
/var/log/osquery
```

#### Getting file metadata

To get file metadata (e.g. `/usr/bin/osqueryi`)

```python
import hodgepodge.files
import json

from hodgepodge.json_encoder import JSONEncoder

file = hodgepodge.files.get_file_metadata(
    path='/usr/bin/osqueryi',
    include_size=True,
    include_hashes=True,
    hash_algorithms=['md5', 'sha1', 'sha256', 'blake2s', 'blake2b'],
)
print(json.dumps(file, cls=JSONEncoder))
```

```json
{
  "path": "/usr/bin/osqueryi",
  "name": "osqueryi",
  "directory": "/usr/bin",
  "size": 94622168,
  "hashes": [
    {
      "algorithm": "md5",
      "value": "c2b3d560ac763c2963a910ef1c26ad7f"
    },
    {
      "algorithm": "sha1",
      "value": "d1cd742e947bbf7a53e6fb45c447b72514d1ef3c"
    },
    {
      "algorithm": "sha256",
      "value": "4292648fa8a85843560cc176385a25142803f53068301292d6a0e0d4d39c5fc1"
    },
    {
      "algorithm": "blake2s",
      "value": "d22262a90fa55c924ac10bd553332cb7e6912cffc7ce6beda6dcfaabc66fd8a5"
    },
    {
      "algorithm": "blake2b",
      "value": "5cc452355c48738deebe33956fb6370384844740c1d1ce4c12f7ba730bb357d47ec5d1b07a10c9f86bc07e596d51f3f98933faf8ed2b9a8aa802e2fca428a0a2"
    }
  ]
}
```

#### Hashing files

To hash a file (e.g. `/usr/bin/osqueryi`):

```python
import hodgepodge.hashing
import json

from hodgepodge.json_encoder import JSONEncoder

file = hodgepodge.hashing.get_file_hashes(
    path='/usr/bin/osqueryi',
    algorithms=['md5', 'sha1', 'sha256', 'blake2s', 'blake2b'],
)
print(json.dumps(file, cls=JSONEncoder))
```

```json
[
  {
    "algorithm": "md5",
    "value": "c2b3d560ac763c2963a910ef1c26ad7f"
  },
  {
    "algorithm": "sha1",
    "value": "d1cd742e947bbf7a53e6fb45c447b72514d1ef3c"
  },
  {
    "algorithm": "sha256",
    "value": "4292648fa8a85843560cc176385a25142803f53068301292d6a0e0d4d39c5fc1"
  },
  {
    "algorithm": "blake2s",
    "value": "d22262a90fa55c924ac10bd553332cb7e6912cffc7ce6beda6dcfaabc66fd8a5"
  },
  {
    "algorithm": "blake2b",
    "value": "5cc452355c48738deebe33956fb6370384844740c1d1ce4c12f7ba730bb357d47ec5d1b07a10c9f86bc07e596d51f3f98933faf8ed2b9a8aa802e2fca428a0a2"
  }
]
```

#### Hashing byte strings

To hash a byte string (e.g. `b'Hello World'`):

```python
from hodgepodge.json_encoder import JSONEncoder

import hodgepodge.hashing
import json

hashes = hodgepodge.hashing.get_hashes(
    data=b'Hello World',
    algorithms=['md5', 'sha256'],
)
print(json.dumps(hashes, cls=JSONEncoder))
```

```json
[
  {
    "algorithm": "md5",
    "value": "b10a8db164e0754105b7a99be72e3fe5"
  },
  {
    "algorithm": "sha256",
    "value": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
  }
]
```

#### Reading and writing `polars.DataFrame` objects

`polars` provides a fast and efficient DataFrame implementation for Python. 

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

#### Converting JSON files into Parquet files

To convert files from JSON format into Parquet format:

1. Read the JSON file into a `polars.DataFrame`
2. Write the `polars.DataFrame` to a Parquet file

```python
import hodgepodge.dataframes
import hodgepodge.files
import os

directory = hodgepodge.files.get_real_path('~/src/data/layers/silver/stix2/mitre-attack-enterprise/intrusion-set')
input_file = os.path.join(directory, 'stix2-bundle.json')
output_file = os.path.join(directory, 'stix2-bundle.parquet')

df = hodgepodge.dataframes.read_dataframe(input_file)
hodgepodge.dataframes.write_dataframe(df, output_file)
```

As an example of how to query the converted Parquet file using [DuckDB](https://duckdb.org/):

- Create a table named `intrusion_sets`
- Select all records from the `intrusion_sets` table where a row contains an alias beginning with 'FIN' (e.g. FIN7):

```
duckdb
```

```sql
CREATE OR REPLACE TABLE intrusion_sets AS (
  SELECT
    o.*
  FROM (
    SELECT 
      UNNEST(objects) AS o
    FROM '~/src/data/layers/silver/stix2/mitre-attack-enterprise/intrusion-set/stix2-bundle.parquet'
  )
);
```

```sql
SELECT
  "name",
  "aliases"
FROM intrusion_sets
WHERE "name" LIKE 'FIN%';
```

```
┌─────────┬────────────────────────────────────────────────────────────────────────────┐
│  name   │                                  aliases                                   │
│ varchar │                                 varchar[]                                  │
├─────────┼────────────────────────────────────────────────────────────────────────────┤
│ FIN10   │ [FIN10]                                                                    │
│ FIN13   │ [FIN13, Elephant Beetle]                                                   │
│ FIN4    │ [FIN4]                                                                     │
│ FIN5    │ [FIN5]                                                                     │
│ FIN6    │ [FIN6, Magecart Group 6, ITG08, Skeleton Spider, TAAL, Camouflage Tempest] │
│ FIN7    │ [FIN7, GOLD NIAGARA, ITG14, Carbon Spider, ELBRUS, Sangria Tempest]        │
│ FIN8    │ [FIN8, Syssphinx]                                                          │
└─────────┴────────────────────────────────────────────────────────────────────────────┘
```
