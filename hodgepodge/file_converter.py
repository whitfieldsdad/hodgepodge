
from typing import Iterable, Optional
from hodgepodge import dataframes
from hodgepodge.constants import FILE_TYPES_TO_FILE_EXTENSIONS
import hodgepodge.files
import polars as pl
from polars.exceptions import PanicException
import os


def auto_convert_files(
        input_dir: str, 
        input_file_type: str,
        output_file_type: str,
        input_compression_type: Optional[str] = None, 
        output_compression_type: Optional[str] = None):

    input_dir = hodgepodge.files.get_real_path(input_dir)

    input_file_extension = FILE_TYPES_TO_FILE_EXTENSIONS[(input_file_type, input_compression_type)]
    input_file_pattern = f'*{input_file_extension}'
    
    input_files = hodgepodge.files.iter_file_paths(input_dir, filename_patterns=[input_file_pattern])
    convert_files(input_files, output_file_type=output_file_type, output_compression_type=output_compression_type)


def convert_files(input_paths: Iterable[str], output_file_type: str, output_compression_type: Optional[str] = None):
    for input_path in input_paths:
        output_path = hodgepodge.files.replace_file_extension(
            input_path=input_path,
            output_file_type=output_file_type,
            output_compression_type=output_compression_type,
        )
        try:
            convert_file(input_path, output_path)
        except (Exception, PanicException) as e:
            continue


def convert_file(input_path: str, output_path: Optional[str] = None, output_file_type: Optional[str] = None, output_compression_type: Optional[str] = None) -> None:
    if not (output_path or output_file_type):
        raise ValueError("output_path or output_file_type must be provided")

    input_path = hodgepodge.files.get_real_path(input_path)

    try:
        df = dataframes.read_dataframe(input_path)
        dataframes.write_dataframe(
            df=df, 
            path=output_path, 
            file_type=output_file_type, 
            compression_type=output_compression_type,
        )
    except (Exception, PanicException) as e:
        raise RuntimeError(f"Failed to convert {input_path} to {output_path}") from e


if __name__ == "__main__":
    import click

    @click.group()
    def main():
        pass

    @main.command()
    @click.option('-i', "--input-dir", required=True, type=click.Path(exists=True))
    @click.option("--input-file-type", required=True, type=str)
    @click.option("--input-compression-type", required=False, type=str)
    @click.option("--output-file-type", required=True, type=str)
    @click.option("--output-compression-type", required=False, type=str)
    def bulk_convert(
        input_dir: str, 
        input_file_type: str, 
        output_file_type: str, 
        input_compression_type: Optional[str] = None, 
        output_compression_type: Optional[str] = None):
        """
        Bulk convert dataframe files with polars
        """
        auto_convert_files(
            input_dir=input_dir,
            input_file_type=input_file_type,
            output_file_type=output_file_type,
            input_compression_type=input_compression_type,
            output_compression_type=output_compression_type,
        )
    
    main()
