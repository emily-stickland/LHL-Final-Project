import pandas as pd 
import numpy as np


def clean_offence_codes(df):
    # Remove white spaces from the 'In Custody' column and trailing white spaces
    df['Offence Number'] = df['Offence Number'].str.strip().str.rstrip()

    # Drop NaNs and display result
    before = len(df)
    df.dropna (subset=['Offence Number'], inplace=True)
    after = len(df)
    num_dropped = before - after
    print(f"{num_dropped} rows have been dropped")

    return df


def encode_offences(df):

    # encode Discharge Available as 0 and unavailable as 1
    df['Discharge Available'] = df['CSO Available'].map({'Y': 0, 'N': 1}).astype(int)

    # encode Suspended Sentence available as 0 and unavailable as 1
    df['SS Available'] = df['CSO Available'].map({'Y': 0, 'N': 1}).astype(int)

    # encode CSO available as 0 and unavailable as 1
    df['CSO Available'] = df['CSO Available'].map({'Y': 0, 'N': 1}).astype(int)

    # encode indictble as 2, hybrid and summary as 0
    df['Election'] = df['Election'].map (   \
        {'Summary': 0, 
         'Hybrid': 1,
         'Indictable' : 3 }  ).astype(int)

    return df



def compare_dataframes(df, lookup_df):
    
    # compare the values of col1 in df1 with the values of col2 in df2
    in_both = df['Offence Number'].isin(lookup_df['Offence Number'])
    in_df_only = df['Offence Number'][~in_both]

    # print the number of values in df1 that appear in df2 and the number of values in df1 that do not appear in df2
    print(f"Number of values in both dataframes (to keep): {in_both.sum()}")
    print(f"Number of values not in lookup df (to drop): {len(in_df_only)}")

    # Get unique values of 'Offence Number' in df1 that are not in df2
    unique_values = df.loc[~df['Offence Number'].isin(lookup_df['Offence Number']), 'Offence Number'].unique()
    print(f"Offences that have no lookup and are being dropped: {unique_values}")

    # drop the rows that only appear in lookup_df
    df = df[df['Offence Number'].isin(lookup_df['Offence Number'])]

    return df



def clean_jail_time(df):
    # replace NaNs with 0
    df['Maximum (Summary)(Months)'] = df['Maximum (Summary)(Months)'].fillna(0)
    df['Maximum (Indictable)(Years)'] = df['Maximum (Indictable)(Years)'].fillna(0)

    # convert jail time to int
    df['Maximum (Summary)(Months)'] = df['Maximum (Summary)(Months)'].astype(int)
    df['Maximum (Indictable)(Years)'] = df['Maximum (Indictable)(Years)'].astype(int)

    return df