import argparse
import logging
from scrapper import (
    get_scores_table,
    write_file,
    get_match_awards_table,
    get_match_results_table,
    get_dismissal_list,
    transform_data,
)
import pandas as pd

logging.basicConfig(
    level="DEBUG",
    format="""%(asctime)s | %(levelname)s | %(name)s - %(message)s""",
)
log = logging.getLogger(__name__)

if __name__ == "__main__":

    log.info("Started process...")

    parser = argparse.ArgumentParser()
    parser.add_argument("--fileformat")

    args = parser.parse_args()

    file_format = args.fileformat

    if file_format not in ("csv", "parquet"):
        log.error("Invalid file format. Please use 'csv' or 'parquet'.")
        raise ValueError("Invalid file format. Please use 'csv' or 'parquet'.")

    log.debug("Started scrapping...")
    scores_df = get_scores_table()

    write_file(scores_df, f"scores.{file_format}")

    match_awards_df = get_match_awards_table()

    write_file(match_awards_df, f"match_awards.{file_format}")

    match_results_df = get_match_results_table()

    write_file(match_results_df, f"match_results.{file_format}")

    dismissal_list_df = get_dismissal_list()

    write_file(dismissal_list_df, f"dismissal_list.{file_format}")

    rohit_sharma_career_df = transform_data(
        scores_df, match_awards_df, match_results_df, dismissal_list_df
    )

    write_file(rohit_sharma_career_df, f"rohit_sharma_career.{file_format}")
