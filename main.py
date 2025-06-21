import argparse
from scrapper import (
    get_scores_table,
    write_file,
    get_match_awards_table,
    get_match_results_table,
)
import pandas as pd

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--fileformat")

    args = parser.parse_args()

    file_format = args.fileformat

    if file_format not in ("csv", "parquet"):
        raise ValueError("Invalid file format. Please use 'csv' or 'parquet'.")

    scores_raw_df = get_scores_table()

    write_file(scores_raw_df, f"scores.{file_format}")

    match_awards_df = get_match_awards_table()

    write_file(match_awards_df, f"match_awards.{file_format}")

    match_results_df = get_match_results_table()

    write_file(match_results_df, f"match_results.{file_format}")
