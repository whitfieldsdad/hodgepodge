import gzip
import json
import os
from typing import Optional, Tuple

import polars as pl
import yaml

from hodgepodge.json_encoder import JSONEncoder
from hodgepodge.constants import CSV, JSON, JSONL, PARQUET, GZIP, YAML


def read_dataframe(path: str, file_type: Optional[str] = None) -> pl.DataFrame:
    """
    Read a dataframe from a file.

    If no file type or compression type is specified it will be inferred from the file extension.
    """
    if not file_type:
        file_type, _ = _get_file_and_compression_type_from_path(path)
        if not file_type:
            raise ValueError(f'Could not infer file type from path: {path}')

    if file_type == CSV:
        df = pl.read_csv(path)
    elif file_type == JSON:
        df = pl.read_json(path)
    elif file_type == JSONL:
        df = pl.read_ndjson(path)
    elif file_type == PARQUET:
        df = pl.read_parquet(path)
    elif file_type == YAML:
        data = yaml.safe_load(open(path))
        df = pl.DataFrame(data)
    else:
        raise ValueError(f'Unsupported file type {file_type} (path: {path})')
    return df


def write_dataframe(
        df: pl.DataFrame, 
        path: str, 
        file_type: Optional[str] = None, 
        compression_type: Optional[str] = None) -> None:
    """
    Write a dataframe to a file.

    If no file type or compression type is specified it will be inferred from the file extension.
    """
    if not file_type:
        file_type, compression_type = _get_file_and_compression_type_from_path(path)
        if not file_type:
            raise ValueError(f'Could not infer file type from path: {path}')
    
    if file_type == CSV and not compression_type:
        df.write_csv(path)
    elif file_type == CSV and compression_type == GZIP:
        df.write_csv(path, compression=compression_type)
    elif file_type == JSON and not compression_type:
        df.write_json(path)
    elif file_type == JSON and compression_type == GZIP:
        rows = df.to_dicts()
        blob = json.dumps(rows, indent=4, sort_keys=True, cls=JSONEncoder).encode('utf-8')
        with gzip.open(path, 'wt', encoding='utf-8') as f:
            f.write(blob.decode('utf-8'))
    elif file_type == JSONL and not compression_type:
        df.write_ndjson(path)
    elif file_type == JSONL and compression_type == GZIP:
        df.write_ndjson(path, compression=compression_type)
    elif file_type == PARQUET:
        df.write_parquet(path, compression=compression_type)
    elif file_type == YAML:
        rows = df.to_dicts()
        with open(path, 'w') as f:
            yaml.dump(rows, f)
    else:
        raise ValueError(f'Unsupported file and compression type combo (file type: {file_type}, compression type: {compression_type}, path: {path})')


def _get_file_and_compression_type_from_path(path: str) -> Tuple[Optional[str], Optional[str]]:
    filename = os.path.basename(path)
    if filename.endswith('.csv.gz'):
        return CSV, GZIP
    elif filename.endswith('.csv'):
        return CSV, None
    elif filename.endswith('.jsonl.gz'):
        return JSONL, GZIP
    elif filename.endswith('.jsonl'):
        return JSONL, None
    elif filename.endswith('.json.gz'):
        return JSON, GZIP
    elif filename.endswith('.json'):
        return JSON, None
    elif filename.endswith('.parquet'):
        return PARQUET, None
    elif filename.endswith('.yaml'):
        return YAML, None
    else:
        raise ValueError(f"Could not infer file type and compression type from path: {path}")
