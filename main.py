import os
from scrapper import get_table, write_file
import pandas as pd

if __name__ == "__main__":

    columns, data = get_table()

    raw_df = pd.DataFrame(data, columns=columns)

    write_file(raw_df, "raw_data.csv")
