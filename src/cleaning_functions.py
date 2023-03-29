import pandas as pd 
import numpy as np



def split_info(df):
    """
    @ param df
    A function to split the Info column into 4 separate columns - 'Proceeding Type', 'Court', 'Statute', 'Offence Number'
    returns modified df
    """
    df[['Proceeding Type', 'Court', 'Statute', 'Offence Number']] = df['Info'].str.split(n=3, expand=True)
    
    return df




def drop_cols(df):
    """
    A param df
    A function to drop specified columns
    returnd modified df
    """

    df.drop(columns = ["Videoconf", "Info", "File", "Name", "Lawyer", 'Statute_x', 'Statute_y'], inplace=True)
    print ("columns: 'Videoconf', 'Info', 'File', 'Name', 'Lawyer', and 'Statute' have been dropped")
    return df




def impute_days_in_court(df):
    """
    @ param df
    A function to fill the number of days in court with the mean of the column
    returns modified df, and prints the number of rows that have been dropped
    """

    #df['Days in Court'] = df['Days in Court'].astype(int)

    # Calculate the mean of Days in Court column
    mean_days_in_court = df['Days in Court'].mean()

    # Replace the NaN values with the mean
    df['Days in Court'].fillna(mean_days_in_court, inplace=True)

    # Convert the 'Days in Court' column back to integer
    df['Days in Court'] = df['Days in Court'].astype(int)

    return df





def clean_lawyers(df):
    """
    @ param df
    A function to remove punctuation and whitespace from the Lawyer column
    Returns clean column, plus a second column that indicates whether an accused has a lawyer (1) or not (0)
    returns modified df
    """
    
    # remove punctuation and initials from Lawyer column
    df['Lawyer'] = df['Lawyer'].str.replace(r'[^\w\s]','').str.replace(r'\b\w{1,2}\b','')
    
    # create a numeric column to indicate if the accused has a lawyer
    df['Has Lawyer'] = np.where(df['Lawyer'].isna(), 0, 1)

    # change NaNs to empty string
    df['Lawyer'].fillna('', inplace=True)

    return df



def preprocess_release_type(df):
    """
    @ param df
    A function to clean the Release Type column
    Removes whitespace, deletes empty strings and fills NaNs with UNK
    returns modified df
    """
    # remove punctuation
    df['Bail Status'] = df['Bail Status'].str.replace(r'[^\w\s]','')

    # Remove white spaces from the 'In Custody' column and trailing white spaces
    df['Bail Status'] = df['Bail Status'].str.strip().str.rstrip()

    # delete empty strings
    df['Bail Status'] = np.delete(df['Bail Status'], np.where(df['Bail Status'] == '')[0])
    
    # replace NaN values with 'UNK'
    df['Bail Status'].fillna('UNK', inplace=True)
    
    return df




def clean_incustody(df):
    """
    @ param df
    A function to clean but not encode the In Custody column
    Drops NaNs and empty strings
    prints number of dropped rows
    Returns modified df with values of 1 : in custody, and 0 : not in custody
    returns 
    """

    before = len(df)

    # drop NaNs
    df.dropna(subset=['In Custody'], inplace=True)

    # remove whitespace
    df['In Custody'] = df['In Custody'].str.strip().str.rstrip()

    # create a boolean mask to identify rows with empty strings
    mask = (df['In Custody'] == '')

    # drop rows with missing values or empty strings/spaces
    df.drop(df[mask].index, inplace=True)

    # display number of dropped rows
    after = len(df)
    num_dropped = before - after
    print(f"{num_dropped} rows have been dropped")

    # create a dictionary to map Y to 1 and N to 0 and replace the values
    mapping = {'Y': 1, 'N': 0}
    df['In Custody'] = df['In Custody'].replace(mapping)

    return df




def clean_offence_codes(df):
    """ 
    @ param: df
    A function to drop rows where the Offence Number does not match the specified format
    i.e. at least two digits followed by other characters
    (unless the offence is in the CDSA (Controlled Drugs and Substances Act) where offence numbers have a different pattern
    display number of dropped rows 
    returns modified df)
    """
    # Remove white spaces from the 'In Custody' column and trailing white spaces
    df['Offence Number'] = df['Offence Number'].str.strip().str.rstrip()

    # initialize counter
    before = len(df)

    # Drop NaNs
    df = df.dropna(subset=['Offence Number'])
    df = df[df['Offence Number'].notna()]

    # Drop empty strings
    df = df[df['Offence Number'] != '']

    # Drop word that only contain a single character tarts with a single digit followed by whitespace
    # but only if Statute is not "CDS"
    df = df[~((df['Offence Number'].str.match(r'^\d\s')) & (df['Statute'] != 'CDS') | (df['Offence Number'].str.len() == 1))]

    # count and display results
    after = len(df)
    num_dropped = before - after
    print(f"{num_dropped} rows have been dropped")

    return df