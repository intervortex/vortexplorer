
NONUSER_COLS = [
    'rank', 'artist', 'album', 'year', 'day',
    'lists', 'votes', 'avg', 'wavg', 'rec', 'yt link'
]


def process_spreadsheet(df, spreadsheet_name):
    if spreadsheet_name == 'GOAT':
        return df.drop([0,
                        1]).dropna(axis='columns', thresh=int(0.4 * len(df)))
    elif spreadsheet_name == 'Reliquary':
        return df.drop([0,1,2]).dropna(axis='columns', thresh=int(0.2 * len(df)))
    elif spreadsheet_name == 'Guts':
        return df.drop([0,1]).dropna(axis='columns', thresh=int(0.2 * len(df)))



def process_users(dct):
    print(list(dct.keys()))
    print([usr for usr in dct.keys() if usr.lower() not in NONUSER_COLS])

    return [usr for usr in dct.keys() if usr.lower() not in NONUSER_COLS]
