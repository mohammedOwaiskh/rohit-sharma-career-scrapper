from scrapper import get_scores_table, write_file
import pandas as pd

if __name__ == "__main__":

    columns, data = get_scores_table()

    raw_df = pd.DataFrame(data, columns=columns)

    write_file(raw_df, "raw_data.csv")
    write_file(raw_df, "raw_data.parquet")
