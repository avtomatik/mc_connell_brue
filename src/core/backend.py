from functools import cache

import pandas as pd
from core.classes import Token


@cache
def read_usa_hist(token: Token) -> pd.DataFrame:
    """
    Retrieves Data from Enumerated Historical Datasets
    Parameters
    ----------
    token : Token

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    """

    return pd.read_csv(**token.get_kwargs())


def pull_by_series_id(df: pd.DataFrame, series_id: str) -> pd.DataFrame:
    """


    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    series_id : str

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================
    """
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id].iloc[:, [1]].rename(
        columns={'value': series_id}
    )


def stockpile_usa_hist(series_ids: dict[str, Token]) -> pd.DataFrame:
    """
    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.
    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================
    """
    return pd.concat(
        map(
            lambda _: read_usa_hist(_[-1]).pipe(pull_by_series_id, _[0]),
            series_ids.items()
        ),
        axis=1,
        sort=True
    )
