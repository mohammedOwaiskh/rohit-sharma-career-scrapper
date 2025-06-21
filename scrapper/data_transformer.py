import pandas as pd
from .utils import get_output_filepath


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
    else:
        raise ValueError(f"Unsupported file format {extension}")
