from datetime import datetime
import pandas as pd

from src.palette import palette


def generate_overview_tbl(data, sel_year, sel_stats, column="AVG"):

    dff = pd.DataFrame({
        key: data[col]
        for key, col in zip(
            ["Released", "Artist", "Album", "AVG", "Votes"],
            ["Released", "Artist", "Album", column, "Votes"],
        )
    })

    year_fmt = "%Y"

    try:
        dff["Released"] = pd.to_datetime(dff["Released"], format="%Y")
    except:
        year_fmt = '%b-%m'
        dff["Released"] = pd.to_datetime(dff["Released"], format="%b-%d-%Y")

    if sel_year is not None:
        one = datetime.strptime(sel_year["range"]['x'][1][:10], "%Y-%m-%d")
        two = datetime.strptime(sel_year["range"]['x'][0][:10], "%Y-%m-%d")
        if one < two:
            dff = dff[dff['Released'].between(one, two)]
        else:
            dff = dff[dff['Released'].between(two, one)]

    if sel_stats is not None:
        start = sel_stats["range"]['x'][0]
        end = sel_stats["range"]['x'][1]
        dff = dff[dff[column].between(start, end)]

    dff['Released'] = dff['Released'].apply(lambda x: x.strftime(year_fmt))
    return dff.to_dict('records')
