import gzip
import json
from typing import Optional

import polars as pl
import yaml

from hodgepodge.json_encoder import JSONEncoder
from hodgepodge.constants import CSV, JSON, JSONL, PARQUET, GZIP, YAML, FILE_EXTENSIONS_TO_FILE_TYPES
import hodgepodge.files


def read_dataframe(path: str, file_type: Optional[str] = None) -> pl.DataFrame:
    """
    Read a dataframe from a file.

    If no file type or compression type is specified it will be inferred from the file extension.
    """
    if not file_type:
        file_type, _ = hodgepodge.files.get_file_and_compression_type_from_path(path)
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
        file_type, compression_type = hodgepodge.files.get_file_and_compression_type_from_path(path)
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


def replace_binary_dtype(dtype: pl.DataType, target: pl.DataType = pl.String) -> pl.DataType:
    if dtype == pl.Binary:
        return target
    if isinstance(dtype, pl.List):
        return pl.List(replace_binary_dtype(dtype.inner, target))
    if isinstance(dtype, pl.Array):
        return pl.Array(replace_binary_dtype(dtype.inner, target), dtype.shape)
    if isinstance(dtype, pl.Struct):
        return pl.Struct([
            pl.Field(field.name, replace_binary_dtype(field.dtype, target))
            for field in dtype.fields
        ])
    return dtype


if __name__ == "__main__":
    pass