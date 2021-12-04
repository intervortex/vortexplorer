import pandas as pd

from data.sheets import sheets_list

NONUSER_COLS = [
    'rank', 'artist', 'album', 'year', 'day', 'lists', 'votes', 'avg', 'wavg', 'released', 'genre',
    'label', 'rec', 'yt link'
]


def process_spreadsheet(df, spreadsheet_name):
    """Standardize spreadsheets to a base format."""

    sheet = sheets_list[spreadsheet_name]

    # Standardize time column and remove unneeded columns
    df = df.rename(columns={sheet['time_col']: 'Released'}, ).drop(sheet['header_remove'])

    # check time for any problems
    is_NaN = df['Released'].isnull()
    row_has_NaN = is_NaN.any()
    if row_has_NaN:
        rows_with_NaN = df[is_NaN]
        from src.notifications import notify
        notify(f"Malformed date rows in <{spreadsheet_name}>:\n{rows_with_NaN[['Artist','Album']]}")
        return pd.DataFrame(columns=NONUSER_COLS)

    # Append year to column with no release date
    fmt = "%Y"
    if sheet['time_col'] == 'Released':
        fmt = "%b-%d-%Y"
        df['Released'] = df['Released'].apply(lambda x: str(x) + '-' + spreadsheet_name)

    # Format time correctly
    try:
        df['Released'] = pd.to_datetime(df['Released'], format=fmt)

    except ValueError as e:
        from src.notifications import notify
        notify(f"Cannot convert date in <{spreadsheet_name}>:\n{e}")
        return pd.DataFrame(columns=NONUSER_COLS)

    # Drop votes from users which have not voted enough
    user_cutoff = min(int(sheet['thresh'] * len(df)), 100)
    df = df.dropna(axis='columns', thresh=user_cutoff)

    # Check unique
    duplicates = df.duplicated(subset=['Artist', 'Album'])
    if any(duplicates):
        from src.notifications import notify
        notify(
            f"Duplicate albums in {spreadsheet_name}: {df[duplicates][['Artist', 'Album']].values}"
        )

    return df


def process_users(dct):

    return [usr for usr in dct.keys() if usr.lower() not in NONUSER_COLS]
