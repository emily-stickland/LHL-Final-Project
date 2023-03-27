import pandas as pd 
import numpy as np


# Split the Info column into three new columns
def split_info(df):
    df[['Proceeding', 'Court', 'Statute', 'Offence Number']] = df['Info'].str.split(n=3, expand=True)
    return df


# drop columns
def drop_cols(df):
    df.drop(columns = ["Videoconf", "Info", "File", "Name", "Lawyer", 'Statute_x', 'Statute_y'], inplace=True)
    print ("columns: 'Videoconf', 'Info', 'File', 'Name', 'Lawyer', and 'Statute' have been dropped")
    return df



# define function to drop rows with null values for Days in Court or Offence Number
def drop_null_rows(df):
    before = len(df)

    df.dropna(subset=['Days in Court', 'Offence Number'], inplace=True)
    df['Days in Court'] = df['Days in Court'].astype(int)
    after = len(df)
    
    num_dropped = before - after
    print(f"{num_dropped} rows have been dropped")
    return df



# define function to deal with lawyers

def clean_lawyers(df):
    
    # remove punctuation and initials from Lawyer column
    df['Lawyer'] = df['Lawyer'].str.replace(r'[^\w\s]','').str.replace(r'\b\w{1,2}\b','')
    
    # create a numeric column to indicate if the accused has a lawyer
    df['Has Lawyer'] = np.where(df['Lawyer'].isna(), 0, 1)

    # change NaNs to empty string
    df['Lawyer'].fillna('', inplace=True)

    return df



def bail_status(df):
    # remove punctuation
    df['Bail Status'] = df['Bail Status'].str.replace(r'[^\w\s]','')

    # Remove white spaces from the 'In Custody' column and trailing white spaces
    df['Bail Status'] = df['Bail Status'].str.strip().str.rstrip()

    # delete empty strings
    df['Bail Status'] = np.delete(df['Bail Status'], np.where(df['Bail Status'] == '')[0])
    
    # replace NaN values with 'UNK'
    df['Bail Status'].fillna('UNK', inplace=True)
    
    return df




# define function to one-hot encode In Custody column

def encode_incustody(df):
    """ 
    @ param: df
    A function to one-hot encode whether someone is in custody, not in custody or
    custodial status is unknown
    return df)
    """
    # Replace NaNs with U
    df['In Custody'].fillna('U', inplace=True)
 
    # Remove white spaces from the 'In Custody' column
    df['In Custody'] = df['In Custody'].str.strip()

    # Replace empty strings with U
    df['In Custody'] = df['In Custody'].replace('', 'U')

    # One-hot encode In Custody column
    custody_df = pd.get_dummies(df['In Custody'], prefix='custody')

    # Concatenate encoded column to original dataframe
    df = pd.concat([df, custody_df], axis=1)

    # Rename columns
    df.rename(columns = {'custody_N': 'Not in Custody',
                         'custody_Y': 'Is In Custody',
                         'custody_U': 'Custody Unknown'}, inplace=True)
    
    df.drop(columns ='In Custody', inplace = True)

    return df



# define function to one-hot encode Court Location column

def encode_courts(df):
    """ 
    @ param: df
    A function to clean and one-hot encode the court location
    return df)
    """
 
    # Remove white spaces from the 'Court Location' column
    df['Court Location'] = df['Court Location'].str.strip()

    # One-hot encode Court Location column
    court_df = pd.get_dummies(df['Court Location'])

    # Concatenate encoded column to original dataframe
    df = pd.concat([df, court_df], axis=1)
    
    # drop the original column
    df.drop(columns ='Court Location', inplace = True)

    return df



def clean_offence_codes(df):
    """ 
    @ param: df
    A function to drop rows where the Offence Number does not match the specified format
    i.e. at least two digits followed by other characters
    (unless the offence is in the CDSA (Controlled Drugs and Substances Act) where offence numbers have a different pattern
    display number of dropped rows 
    return df)
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