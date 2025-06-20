import os
import re


def get_output_filepath(filename: str):

    filepath = os.path.join(os.getcwd(), "output", filename)

    if not re.match(r"^\w+\.(csv|parquet)$", filename):
        raise ValueError("Filename must contain an extension (either .csv or .parquet")

    extension = filename.split(".")[1]

    return filepath, extension
