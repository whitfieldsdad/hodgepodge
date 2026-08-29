from unittest import TestCase
from hodgepodge import dataframes

import polars as pl
import tempfile


class TestDataFrames(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = pl.DataFrame({
            "fruit": ["apple", "banana", "blueberry"],
            "colour": ["red", "yellow", "blue"],
            "quantity": [10, 7, 5]
        })

    def test_read_write_dataframe_with_csv_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as file:
            dataframes.write_dataframe(self.df, file.name)
            file.flush()
            
            df = dataframes.read_dataframe(file.name)
            self.assertEqual(df.shape, (3, 3))
            self.assertEqual(set(df.columns), {'fruit', 'colour', 'quantity'})

    def test_read_write_dataframe_with_json_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json') as file:
            dataframes.write_dataframe(self.df, file.name)
            file.flush()
            
            df = dataframes.read_dataframe(file.name)
            self.assertEqual(df.shape, (3, 3))
            self.assertEqual(set(df.columns), {'fruit', 'colour', 'quantity'})

    def test_read_write_dataframe_with_jsonl_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.jsonl') as file:
            dataframes.write_dataframe(self.df, file.name)
            file.flush()
            
            df = dataframes.read_dataframe(file.name)
            self.assertEqual(df.shape, (3, 3))
            self.assertEqual(set(df.columns), {'fruit', 'colour', 'quantity'})

    def test_read_write_dataframe_with_parquet_file(self):
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.parquet') as file:
            dataframes.write_dataframe(self.df, file.name)
            file.flush()
            
            df = dataframes.read_dataframe(file.name)
            self.assertEqual(df.shape, (3, 3))
            self.assertEqual(set(df.columns), {'fruit', 'colour', 'quantity'})

    def test_read_write_dataframe_with_yaml_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml') as file:
            dataframes.write_dataframe(self.df, file.name)
            file.flush()
            
            df = dataframes.read_dataframe(file.name)
            self.assertEqual(df.shape, (3, 3))
            self.assertEqual(set(df.columns), {'fruit', 'colour', 'quantity'})
