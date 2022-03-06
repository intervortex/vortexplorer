# How to get the sheets in a CSV format
sheets_template = "https://docs.google.com/spreadsheet/ccc?key={0}&output=csv"

# A list of G sheets
sheets_list = {
    '2022': {
        'url': "1TZ6JzeC-BxUSwSbwaNvTfUGz0J4CVd3oCPVduLJzDLg",
        'header_remove': [0, 1],
        'thresh': 0.1,
        'time_col': 'Released',
    },
    'RSCC': {
        'url': "11RuUuH_40HPF5qQ0n8oTSqLhIia6JNMI89Cf6xiPqP4",
        'header_remove': [0, 1],
        'thresh': 0.3,
        'time_col': 'Year',
        'main_col': 'Song',
    },
    '2021': {
        'url': "1I9OAFHol_LMXua0rmSl2yFiOkHDrgMHETrgL7NXYCsA",
        'header_remove': [0, 1],
        'thresh': 0.1,
        'time_col': 'Released',
    },
    '2020': {
        'url': "1XRWlCGM4QRetcN_PBZAG30MZbzrUzq968Fs2Q38OBXU",
        'header_remove': [0, 1],
        'thresh': 0.1,
        'time_col': 'Released',
    },
    'Reliquary': {
        'url': "13T9MFuhDTuQe_21s58KcX6KiiT2w_HvfiQ9AjEbuzYM",
        'header_remove': [0, 1, 2],
        'thresh': 0.2,
        'time_col': 'Year',
    },
    'Guts': {
        'url': "18se3f36hUJsTLLoXnYrxKaH_YowWk5HvzqX1jugs72w",
        'header_remove': [0, 1],
        'thresh': 0.2,
        'time_col': 'Year',
    },
    '2019': {
        'url': "1EaKDK7P16_TGfZmlFSzgalQrOo8vT2YAlcMxxk9PmQ4",
        'header_remove': [0, 1],
        'thresh': 0.1,
        'time_col': 'Released',
    },
    'GOAT': {
        'url': "1F_7q1tP7zoy3sJKIAJa2XJ5NbyAGASvmiglSJSneh2U",
        'header_remove': [0, 1],
        'thresh': 0.4,
        'time_col': 'Year',
    },
    '2018': {
        'url': "18SjPH_m9oO49TR-hfJKbpCCN4XKDNQv-MJREPA7rqbE",
        'header_remove': [0, 1],
        'thresh': 0.1,
        'time_col': 'Released',
    },
}


def get_sheet_csv(spreadsheet_name):
    return sheets_template.format(sheets_list[spreadsheet_name]['url'])