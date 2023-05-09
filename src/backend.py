from functools import cache

import pandas as pd
from pandas import DataFrame

from constants import MAP_READ_USA_HIST


@cache
def read_usa_hist(filepath_or_buffer: str) -> DataFrame:
    """
    Retrieves Data from Enumerated Historical Datasets
    Parameters
    ----------
    filepath_or_buffer : str

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    """
    kwargs = {
        'filepath_or_buffer': filepath_or_buffer,
        'header': 0,
        'names': tuple(MAP_READ_USA_HIST.get(filepath_or_buffer).keys()),
        'index_col': 1,
        'skiprows': (0, 4)[filepath_or_buffer == 'dataset_usa_brown.zip'],
        'usecols': tuple(MAP_READ_USA_HIST.get(filepath_or_buffer).values()),
    }
    return pd.read_csv(**kwargs)


def pull_by_series_id(df: DataFrame, series_id: str) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    series_id : str

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================
    """
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id].iloc[:, [1]].rename(
        columns={"value": series_id}
    )


def stockpile_usa_hist(series_ids: dict[str, str]) -> DataFrame:
    """
    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.
    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================
    """
    return pd.concat(
        map(
            lambda _: read_usa_hist(_[1]).pipe(pull_by_series_id, _[0]),
            series_ids.items()
        ),
        axis=1,
        sort=True
    )
