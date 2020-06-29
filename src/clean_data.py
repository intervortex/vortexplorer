from sheets import spreadsheet_list

NONUSER_COLS = [
    'rank', 'artist', 'album', 'year', 'day', 'lists', 'votes', 'avg', 'wavg',
    'released', 'genre', 'label', 'rec', 'yt link'
]


def process_spreadsheet(df, spreadsheet_name):

    df = df.rename(
        columns={
            spreadsheet_list[spreadsheet_name]['time_col']: 'Released'
        },
    ).drop(spreadsheet_list[spreadsheet_name]['header_remove'])

    if spreadsheet_list[spreadsheet_name]['time_col'] == 'Released':
        df['Released'] = df['Released'].apply(
            lambda x: x + '-' + spreadsheet_name
        )

    return df.dropna(
        axis='columns',
        thresh=min(
            int(spreadsheet_list[spreadsheet_name]['thresh'] * len(df)), 100
        )
    )


def process_users(dct):

    return [usr for usr in dct.keys() if usr.lower() not in NONUSER_COLS]
