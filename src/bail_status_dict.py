def map_bail(df):

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

    df['Bail Status'] = df['Bail Status'].map(bail_status_dict)
    return df
