CSV = 'csv'
JSON = 'json'
JSONL = 'jsonl'
PARQUET = 'parquet'
YAML = 'yaml'

GZIP = 'gzip'
ZSTD = 'zstd'

FILE_EXTENSIONS_TO_FILE_TYPES = {
    '.csv': (CSV, None),
    '.csv.gz': (CSV, GZIP),
    '.json': (JSON, None),
    '.json.gz': (JSON, GZIP),
    '.jsonl': (JSONL, None),
    '.jsonl.gz': (JSONL, GZIP),
    '.parquet': (PARQUET, None),
    '.yaml': (YAML, None),
    '.yaml.gz': (YAML, GZIP),
    '.yml': (YAML, None),
    '.yml.gz': (YAML, GZIP)
}
FILE_TYPES_TO_FILE_EXTENSIONS = {v: k for k, v in FILE_EXTENSIONS_TO_FILE_TYPES.items()}

JSON_INDENT = 4
