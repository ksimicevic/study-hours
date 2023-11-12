import argparse

import numpy as np
import pandas as pd


def group_by_timerange(_df: pd.DataFrame, timerange: str) -> pd.DataFrame:
    _ret_df = _df
    _ret_df['Duration [hrs]'] = pd.to_timedelta(_ret_df['Duration [hrs]'], unit='hour')
    _ret_df = _ret_df[['Subject', 'Date', 'Duration [hrs]']].groupby(['Subject', 'Date', pd.Grouper(key='Duration [hrs]', freq=timerange)], as_index=False).sum()
    _ret_df['Date'] = pd.to_datetime(_ret_df['Date'], dayfirst=True)
    _ret_df = _ret_df.sort_values(by=['Date'], ascending=True)
    return _ret_df


def create_2d_yearly_calendar(_df: pd.DataFrame, year: int) -> np.array:
    timeperiod = pd.date_range(_df.iloc[0]['Date'], _df.iloc[-1]['Date'], freq='D').to_series()
    isocalendar = timeperiod.dt.isocalendar()

    calendar_df = _df.set_index(pd.to_datetime(_df['Date'], dayfirst=True))
    calendar_df.drop(labels=['Activity', 'Semester'], axis=1, inplace=True)
    year_isocalendar = isocalendar[isocalendar['year'] == year]
    calendar_df = calendar_df.merge(year_isocalendar, how='right', left_index=True, right_index=True)
    # merge will introduce NaNs on days when no activities occurred
    calendar_df['Duration [hrs]'].fillna(0, inplace=True)
    min_week = year_isocalendar['week'].min()

    # scaling
    calendar_df['week'] = calendar_df['week'] - min_week  # row indexes
    calendar_df['day'] = calendar_df['day'] - 1  # column indexes

    num_rows, num_cols = calendar_df['week'].max() + 1, 7

    calendar_2d_array = calendar_df[['Duration [hrs]', 'week', 'day']].to_numpy()
    array_2d = np.zeros(shape=(num_rows, num_cols))
    for c in calendar_2d_array:
        array_2d[c[1], c[2]] += c[0]
    return array_2d


def create_calendar(_df: pd.DataFrame, out_path: str) -> np.array:
    _df['Date'] = pd.to_datetime(_df['Date'], dayfirst=True)
    years = _df['Date'].dt.year.unique()

    with open(out_path, 'w') as ofile:
        for year in years:
            filter_by_year_df = _df[_df['Date'].dt.year == year]
            array_2d = create_2d_yearly_calendar(filter_by_year_df, year)
            ofile.writelines('\n'.join([','.join([str(col) for col in row]) for row in array_2d]))

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='2D Heatmap Calendar Generator',
        description='Helper script to generate a 2d heatmap calendar from a file.'
    )
    parser.add_argument('path', action='store', help='A path to the csv file')
    parser.add_argument('outpath', action='store', help='A path to 2d array output')

    args = parser.parse_args()
    df = pd.read_csv(args.path, sep=',')
    create_calendar(df, args.outpath)
