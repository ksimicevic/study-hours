import argparse

import numpy as np
import pandas as pd

import calendar

calendar.setfirstweekday(calendar.MONDAY)

def create_calendar_heatmap(_df: pd.DataFrame) -> np.array:
    timeperiod = pd.date_range(_df.iloc[0]['Date'], _df.iloc[-1]['Date'], freq='D').to_series()

    calendar_df = _df.set_index(pd.to_datetime(_df['Date'], dayfirst=True))
    calendar_df = calendar_df['Duration [hrs]'].to_frame()
    calendar_df = calendar_df.merge(timeperiod.to_frame(name='Date'), how='right', left_index=True, right_index=True)

    # merge will introduce NaNs on days when no activities occurred
    calendar_df['Duration [hrs]'].fillna(0, inplace=True)

    calendar_df['Month'] = calendar_df['Date'].dt.month
    calendar_df['Year'] = calendar_df['Date'].dt.year

    months = calendar_df[['Year', 'Month']].groupby(['Year', 'Month']).sum().sort_values(['Year', 'Month'], ascending=[True, True])

    calendar_heatmap = []
    for m in months.iterrows():
        year, month = m[0][0], m[0][1]

        activity_df = calendar_df[(calendar_df['Year'] == year) & (calendar_df['Month'] == month)][['Date', 'Duration [hrs]']].groupby('Date').sum()
        month_heatmap = calendar.monthcalendar(year, month)
        for week_idx in range(len(month_heatmap)):
            for day_idx in range(len(month_heatmap[week_idx])):
                if month_heatmap[week_idx][day_idx] != 0:
                    ts = pd.Timestamp(year=year, month=month, day=month_heatmap[week_idx][day_idx])
                    row = activity_df.iloc[lambda x: x.index == ts]
                    if len(row) == 0:
                        month_heatmap[week_idx][day_idx] = 0
                    else:
                        month_heatmap[week_idx][day_idx] = row['Duration [hrs]'][0]

        calendar_heatmap.append(
            [np.array([year, month]), np.array(calendar.monthcalendar(year, month)), np.array(month_heatmap)]
        )

    return np.array(calendar_heatmap, dtype=object)


def write_calendar_heatmap(_df: pd.DataFrame, out_path: str):
    calendar_3d = create_calendar_heatmap(_df)
    np.save(out_path, calendar_3d)
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
    write_calendar_heatmap(df, args.outpath)
