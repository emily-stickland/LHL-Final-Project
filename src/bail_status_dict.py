def map_release_type(df):
    """
    @ param df
    A function to map the 30 different types of bail/detention/process based on order of severity
    Range = 0 for the lease severe (summons) to 8 for the most severe (detention order)
    Fills missing values with the mean
    returns modified df with numerical values instead of release codes
    """

    bail_status_dict = {
        'DO': 8,
        'RIC': 7,
        'REM': 7,
        'AWW': 6,
        'WAR': 6,
        'WRC': 6,
        'AOI': 6,
        'AOO': 5,
        'ROZ': 5,
        'RSD': 5,
        'ROB': 5,
        'RDS': 4,
        'ROS': 4,
        'RWS': 4,
        'ROX': 4,
        'ROD': 3,
        'RWD': 3,
        'RON': 2,
        'ROW': 2,
        'PPA': 2,
        'OIC': 1,
        'OIU': 1,
        'OR': 0,
        'UTA': 0,
        'PTA': 0,
        'AN': 0,
        'ANU': 0,
        'SMC': 0,
        'SUM': 0,
        'NP': 0
        }

    df['Release Type'] = df['Release Type'].map(bail_status_dict)

    # replace missing values with the mean of the non-missing values
    release_type_mean = df['Release Type'].mean()
    df['Release Type'].fillna(release_type_mean, inplace=True)

    return df
