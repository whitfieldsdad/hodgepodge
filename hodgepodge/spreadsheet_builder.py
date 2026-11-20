from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import json

import dacite
import hodgepodge.dataframes
import hodgepodge.files
import polars as pl
import xlsxwriter

MAX_EXCEL_ROWS = 1_048_576
MAX_EXCEL_COLUMNS = 16_384


@dataclass(frozen=True)
class SheetConfig:
    name: str
    path: str
    enabled: bool = True
    select_columns: Iterable[str] | Mapping[str, str] | None = None
    drop_columns: Iterable[str] | None = None
    replace_nan_with_null: bool = False


@dataclass(frozen=True)
class WorkbookConfig:
    sheets: list[SheetConfig]


def read_workbook_config(path: str | Path) -> WorkbookConfig:
    with open(path, "r", encoding="utf-8") as f:
        return parse_workbook_config(json.load(f))


def parse_workbook_config(data: dict[str, Any]) -> WorkbookConfig:
    return dacite.from_dict(
        data_class=WorkbookConfig,
        data=data,
        config=dacite.Config(strict=True),
    )


def build_workbook(config: WorkbookConfig, output_path: str | Path) -> dict[str, Any]:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sheets: list[tuple[str, pl.DataFrame]] = []
    seen_names: set[str] = set()

    for sheet in config.sheets:
        if not sheet.enabled:
            continue

        _validate_sheet_name(sheet.name, seen_names)
        df = _transform_dataframe(_load_sheet_dataframe(sheet), sheet)

        if df.height > MAX_EXCEL_ROWS:
            raise ValueError(
                f"Sheet {sheet.name!r} has {df.height:,} rows; "
                f"Excel allows at most {MAX_EXCEL_ROWS:,} rows per worksheet."
            )

        if df.width > MAX_EXCEL_COLUMNS:
            raise ValueError(
                f"Sheet {sheet.name!r} has {df.width:,} columns; "
                f"Excel allows at most {MAX_EXCEL_COLUMNS:,} columns per worksheet."
            )

        sheets.append((sheet.name, df))

    if not sheets:
        raise ValueError("Workbook configuration produced no enabled sheets.")

    with xlsxwriter.Workbook(output_path, {"nan_inf_to_errors": True}) as workbook:
        for sheet_name, df in sheets:
            df.write_excel(
                workbook=workbook,
                worksheet=sheet_name,
                table_style="Table Style Medium 9",
                autofit=True,
                float_precision=5,
                dtype_formats={
                    pl.Date: "yyyy-mm-dd",
                },
            )


def _validate_sheet_name(name: str, seen_names: set[str]) -> None:
    forbidden = set(r"[]:*?/\\")

    if not name:
        raise ValueError("Worksheet name cannot be empty.")

    if len(name) > 31:
        raise ValueError(f"Worksheet name {name!r} exceeds Excel's 31-character limit.")

    if any(char in forbidden for char in name):
        raise ValueError(
            f"Worksheet name {name!r} contains an Excel-reserved character."
        )

    if name.casefold() in seen_names:
        raise ValueError(f"Duplicate worksheet name: {name!r}.")

    seen_names.add(name.casefold())


def _load_sheet_dataframe(sheet: SheetConfig) -> pl.DataFrame:
    if sheet.path is None:
        raise ValueError(f'Missing path for sheet {sheet.name!r}')

    path = hodgepodge.files.get_real_path(sheet.path)
    return hodgepodge.dataframes.read_dataframe(path)


def _transform_dataframe(df: pl.DataFrame, sheet: SheetConfig) -> pl.DataFrame:
    
    # Select and/or rename columns
    if sheet.select_columns is not None:
        if isinstance(sheet.select_columns, Mapping):
            missing = set(sheet.select_columns) - set(df.columns)
            if missing:
                raise ValueError(f"Sheet {sheet.name!r} references missing columns: {sorted(missing)}")

            df = df.select(
                pl.col(source).alias(output) for source, output in sheet.select_columns.items()
            )
        else:
            selected_columns = list(sheet.select_columns)
            missing = set(selected_columns) - set(df.columns)
            if missing:
                raise ValueError(
                    f"Sheet {sheet.name!r} references missing columns: "
                    f"{sorted(missing)}"
                )

            df = df.select(selected_columns)

    # Replace NaN values with nulls in float columns
    if sheet.replace_nan_with_null:
        float_columns = [
            name
            for name, dtype in df.schema.items()
            if dtype in (pl.Float32, pl.Float64)
        ]

        if float_columns:
            df = df.with_columns(
                pl.col(name).fill_nan(None).alias(name) for name in float_columns
            )

    # Drop specified columns
    if sheet.drop_columns is not None:
        df = df.drop(sheet.drop_columns)

    return df
