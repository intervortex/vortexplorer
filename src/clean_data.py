from sheets import sheets_list

NONUSER_COLS = [
    'rank', 'artist', 'album', 'year', 'day', 'lists', 'votes', 'avg', 'wavg',
    'released', 'genre', 'label', 'rec', 'yt link'
]


def process_spreadsheet(df, spreadsheet_name):

    sheet = sheets_list[spreadsheet_name]

    df = df.rename(columns={
        sheet['time_col']: 'Released'
    }, ).drop(sheet['header_remove'])

    if sheet['time_col'] == 'Released':
        df['Released'] = df['Released'].apply(
            lambda x: x + '-' + spreadsheet_name
        )

    return df.dropna(
        axis='columns', thresh=min(int(sheet['thresh'] * len(df)), 100)
    )


def process_users(dct):

    return [usr for usr in dct.keys() if usr.lower() not in NONUSER_COLS]
