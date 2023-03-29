import pandas as pd 


def encode_incustody(df):
    """ 
    @ param: df
    A function to clean and one-hot encode the In Custody column
    Returns 3 columns with index 'Is In Custody', 'Not in Custody' and 'Custody Unknown'
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




def encode_courts(df):
    """ 
    @ param: df
    A function to clean and one-hot encode the Court location column
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



def encode_offences(df):
    """
    @ param df
    A function to perform both one-hot and binary encoding on the Offence column (containing 220 unique values)
    returns a tuple of 2 new dfs, 'binary_encoded_df' and 'very_large_df'
    """
    import category_encoders as ce

    # create binary encoder object
    encoder = ce.BinaryEncoder()

    # fit and transform the column
    encoded_offence_df = encoder.fit_transform (df ['Offence'] )

    # concatenate the binary encoded column with the original dataframe
    binary_encoded_df = pd.concat ( [df, encoded_offence_df], axis = 1)

    # print update
    print(f"New dataframe created with {len(binary_encoded_df.columns)} columns")

    # get dummies
    offence_dummies_df = pd.get_dummies (df ['Offence'] )

    # concatenate the dummies encoded column with the original dataframe
    very_large_df = pd.concat ( [df, offence_dummies_df], axis = 1)

    # print update
    print(f"New dataframe created with {len(very_large_df.columns)} columns")

    return (binary_encoded_df, very_large_df)

    