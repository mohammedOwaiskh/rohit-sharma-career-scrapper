import dis
import logging
import pandas as pd
from .utils import get_output_filepath

log = logging.getLogger(__name__)


def write_file(df: pd.DataFrame, filename: str):
    """
    Writes a pandas DataFrame to a file in the specified format.
    Parameters:
        df (pd.DataFrame): The DataFrame to be written to file.
        filename (str): The name of the output file (without extension).
        format (str, optional): The file format to write ('csv' or 'parquet'). Defaults to 'csv'.
    Raises:
        ValueError: If an unsupported file format is specified.
    The output file is saved in the 'output' directory within the current working directory.
    """

    filepath, extension = get_output_filepath(filename)

    if extension == "csv":
        df.to_csv(filepath, index=False)
    elif extension == "parquet":
        df.to_parquet(filepath, index=False)

    log.debug(f"Written into file {filename}")


def clean_scores_data(scores: pd.DataFrame):
    log.debug("Cleaning scored data...")

    # remove unncessary columns
    scores = scores.drop(labels=["Mins"], axis=1).copy()

    # drop duplicate rows
    scores.drop_duplicates(inplace=True)

    # remove the matches where Rohit Sharma did not play
    scores = scores[~((scores["Runs"] == "DNB") | (scores["Runs"] == "TDNB"))]

    # Cleaning 'runs' column - remove '*'
    remove_astx = lambda x: x[:-1] if x.endswith("*") else x
    scores.loc[:, "Runs"] = scores["Runs"].apply(remove_astx)

    # Cleaning 'format' column - remove '#'
    remove_hash = lambda x: x.split("#")[0].strip() if "#" in x else x.strip()
    scores.loc[:, "format"] = scores["format"].apply(remove_hash)

    # Cleaning 'SR' column - replace '-' with 0
    scores.loc[:, "SR"] = scores["SR"].replace("-", 0)

    # Cleaning 'Opposition' column - remove 'v' from starting
    scores["Opposition"] = scores["Opposition"].str[2:]

    scores = change_scores_dtypes(scores)

    scores = rename_columns(scores)

    log.debug("Scores data cleaned")
    return scores


def rename_columns(scores: pd.DataFrame):
    renamed_cols = {
        "Runs": "runs",
        "BF": "balls_faced",
        "4s": "fours",
        "6s": "sixes",
        "SR": "strike_rate",
        "Pos": "position_batted",
        "Dismissal": "dismissal_type",
        "Inns": "inning",
        "Opposition": "opposition",
        "Ground": "venue",
        "Start Date": "date",
    }
    scores = scores.rename(renamed_cols, axis=1, copy=True)
    return scores


def change_scores_dtypes(scores: pd.DataFrame):
    convert_dict = {
        "Runs": "int",
        "BF": "int",
        "4s": "int",
        "6s": "int",
        "SR": "float",
        "Pos": "int",
        "Inns": "int",
        "match_id": "int",
    }
    scores = scores.astype(convert_dict, copy=True)

    # Changing data type of "Start Date"
    scores["Start Date"] = pd.to_datetime(scores["Start Date"], format="""%d %b %Y""")

    return scores


def change_awards_dtypes(match_awards: pd.DataFrame):

    convert_dict = {"match_id": "int"}
    match_awards = match_awards.astype(convert_dict, copy=True)

    return match_awards


def change_results_dtypes(match_results: pd.DataFrame):
    convert_dict = {"match_id": "int"}
    match_results = match_results.astype(convert_dict, copy=True)

    return match_results


def change_dissmisal_list_dtypes(dismissal_list: pd.DataFrame):
    convert_dict = {"inning": "int", "match_id": "int"}

    dismissal_list = dismissal_list.astype(convert_dict, copy=True)

    return dismissal_list


def clean_other_data(
    match_awards: pd.DataFrame,
    match_results: pd.DataFrame,
    dismissal_list: pd.DataFrame,
):

    log.debug("Cleaning other data....")

    match_results.drop_duplicates(inplace=True)
    match_results = change_results_dtypes(match_results)

    match_awards.drop_duplicates(inplace=True)
    match_awards = change_awards_dtypes(match_awards)

    dismissal_list.drop_duplicates(inplace=True)
    dismissal_list = change_dissmisal_list_dtypes(dismissal_list)

    log.debug("Cleaned other data....")

    return match_awards, match_results, dismissal_list


def merge_and_clean(
    scores: pd.DataFrame,
    match_awards: pd.DataFrame,
    match_results: pd.DataFrame,
    dismissal_list: pd.DataFrame,
):

    log.debug("Merging dataframes...")
    # Merge all dataframes
    scores_merged = (
        scores.merge(match_results, "left", on="match_id")
        .merge(match_awards, "left", "match_id")
        .merge(dismissal_list, "left", ["match_id", "inning"])
    )

    log.debug("Cleaning the merged data...")
    # Clean potm column
    scores_merged["potm"] = scores_merged["award"].apply(
        lambda x: "yes" if x == "player of the match" else "no"
    )

    # Drop unncessary columns
    scores_merged.drop(
        ["date_y", "date", "award", "dismissal_type_y"], axis=1, inplace=True
    )

    # Rename columns
    scores_merged.rename(
        {"date_x": "date", "dismissal_type_x": "dismissal_type"}, axis=1, inplace=True
    )
    log.debug("Cleaned and returning the merge data...")

    # Return clean and sorted dataframe
    return scores_merged[
        [
            "runs",
            "balls_faced",
            "fours",
            "sixes",
            "strike_rate",
            "position_batted",
            "bowler",
            "dismissal_type",
            "result",
            "potm",
            "date",
            "inning",
            "opposition",
            "venue",
            "format",
        ]
    ].sort_values("date", axis=0)


def transform_data(
    scores: pd.DataFrame,
    match_awards: pd.DataFrame,
    match_results: pd.DataFrame,
    dismissal_list: pd.DataFrame,
):
    """
    Transforms and merges Rohit Sharma's cricket career data from multiple dataframe.
    This function takes in raw dataframes containing scores, match awards, match results,
    and dismissal information, cleans each dataset, and merges them into a single
    comprehensive dataframe representing Rohit Sharma's career statistics.
    Args:
        scores (pd.DataFrame): DataFrame containing raw scores data.
        match_awards (pd.DataFrame): DataFrame containing match awards data.
        match_results (pd.DataFrame): DataFrame containing match results data.
        dismissal_list (pd.DataFrame): DataFrame containing dismissal information.
    Returns:
        pd.DataFrame: A cleaned and merged DataFrame with Rohit Sharma's career data.
    """

    log.debug("Started data and transformation cleaning...")

    scores = clean_scores_data(scores)

    match_awards, match_results, dismissal_list = clean_other_data(
        match_awards, match_results, dismissal_list
    )

    rohit_sharma_career_df = merge_and_clean(
        scores, match_awards, match_results, dismissal_list
    )

    log.debug("Cleaned and Transformed data")

    return rohit_sharma_career_df
