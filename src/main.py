import os

from backend import stockpile_usa_hist
from tools import (calculate_power_function_fit_params_a,
                   calculate_power_function_fit_params_b,
                   calculate_power_function_fit_params_c)

from constants import MAP_MC_CONNEL


def main(year_base: int = 1980, path_src: str = '../data') -> None:
    """
    Power Function Approximation

    Returns
    -------
    None
        DESCRIPTION.
    """
    os.chdir(path_src)

    SERIES_IDS = {
        'Валовой внутренний продукт, млрд долл. США': 'dataset_usa_mc_connell_brue.zip'
    }
    PARAMS = (2800, 0.01, 0.5)
    stockpile_usa_hist(SERIES_IDS).truncate(before=year_base).rename(columns=MAP_MC_CONNEL).pipe(
        calculate_power_function_fit_params_a, PARAMS
    )

    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'dataset_usa_mc_connell_brue.zip',
        'Национальный доход, млрд долл. США': 'dataset_usa_mc_connell_brue.zip',
    }
    PARAMS = (4, 12, 9000, 3000, 0.87)
    stockpile_usa_hist(SERIES_IDS).truncate(before=year_base).rename(columns=MAP_MC_CONNEL).pipe(
        calculate_power_function_fit_params_b, PARAMS
    )

    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'dataset_usa_mc_connell_brue.zip',
        'Валовой объем внутренних частных инвестиций, млрд долл. США': 'dataset_usa_mc_connell_brue.zip',
    }
    PARAMS = (1.5, 19, 1.7, 1760)
    stockpile_usa_hist(SERIES_IDS).truncate(before=year_base).rename(columns=MAP_MC_CONNEL).pipe(
        calculate_power_function_fit_params_c, PARAMS
    )


if __name__ == '__main__':
    main()
