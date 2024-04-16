import numpy as np
import pandas as pd


def transform_datasets(_winter_df: pd.DataFrame, _summer_df: pd.DataFrame) -> pd.DataFrame:
    _winter_df['Semester'] = 'W'
    _summer_df['Semester'] = 'S'
    _df = pd.concat([_winter_df, _summer_df], axis=0)

    _df['Start'] = pd.to_datetime(_df['Date'] + " " + _df['Start'])
    _df['End'] = pd.to_datetime(_df['Date'] + " " + _df['End'])
    _df.insert(3, 'Duration [hrs]', (_df['End'] - _df['Start']) / pd.Timedelta(hours=1))
    return _df


def compute_expected_duration_per_subject(_df: pd.DataFrame, _ects: pd.DataFrame) -> pd.DataFrame:
    _ret_df = _df[['Subject', 'Semester', 'Duration [hrs]']].groupby(['Subject', 'Semester'], as_index=False).sum()
    _ret_df = _ret_df.merge(_ects, on=['Subject'], how='inner')
    _ret_df = _ret_df.sort_values(by=['ECTS', 'Duration [hrs]'], ascending=False)

    _ret_df['Min exp duration [hrs]'] = _ret_df['ECTS'] * 25
    _ret_df['Max exp duration [hrs]'] = _ret_df['ECTS'] * 30
    _ret_df['MinMaxDiff'] = _ret_df['Max exp duration [hrs]'] - _ret_df['Min exp duration [hrs]']
    return _ret_df


def compute_total_duration_per_subject(_df: pd.DataFrame) -> pd.DataFrame:
    _ret_df = _df[['Subject', 'Semester', 'Duration [hrs]']].groupby(['Subject', 'Semester'], as_index=False).sum()
    _ret_df.sort_values(by='Duration [hrs]', ascending=False, inplace=True)
    return _ret_df


def compute_activity(_df: pd.DataFrame) -> pd.DataFrame:
    _ret_df = _df[['Subject', 'Activity', 'Duration [hrs]']].groupby(['Subject', 'Activity'], as_index=False).sum()
    return _ret_df


def filter_by_semester(_df: pd.DataFrame, key: str) -> pd.DataFrame:
    match key:
        case 'winter':
            return _df[_df['Semester'] == 'W']
        case 'summer':
            return _df[_df['Semester'] == 'S']
    return _df


# load the datasets
winter_df = pd.read_csv("data/winter-semester.csv")
summer_df = pd.read_csv("data/summer-semester.csv")
ects_df = pd.read_csv("data/ects.csv")
calendar_heatmap_data = np.load("data/calendar_heatmap.npy", allow_pickle=True)

# transform the dataset
df = transform_datasets(winter_df, summer_df)

expected_and_realised_dur_per_subj_df = compute_expected_duration_per_subject(df, ects_df)
total_dur_per_subj_df = compute_total_duration_per_subject(df)
activity_df = compute_activity(df)
