import pandas as pd
import numpy as np


def apply_selection(df: pd.DataFrame, type_selected: list, start_date, end_date) -> pd.DataFrame:
    # filter data frame according to selection
    df_sub = df[
        (df['type'].isin(type_selected)) \
        & (df['start_date_local'].dt.date>=start_date) & (df['start_date_local'].dt.date<=end_date)
        ].copy()

    # reset index
    df_sub.reset_index(inplace=True)

    return df_sub