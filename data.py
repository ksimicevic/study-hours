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
    _dur_df = _df[['Subject', 'Semester', 'Duration [hrs]']].groupby(['Subject', 'Semester'], as_index=False).sum()
    _dur_df = _dur_df.merge(_ects, on=['Subject'], how='inner')
    _dur_df = _dur_df.sort_values(by=['ECTS', 'Duration [hrs]'], ascending=False)

    _dur_df['Min exp duration [hrs]'] = _dur_df['ECTS'] * 25
    _dur_df['Max exp duration [hrs]'] = _dur_df['ECTS'] * 30
    _dur_df['MinMaxDiff'] = _dur_df['Max exp duration [hrs]'] - _dur_df['Min exp duration [hrs]']
    return _dur_df


def compute_total_duration_per_subject(_df: pd.DataFrame) -> pd.DataFrame:
    ret_df = _df[['Subject', 'Semester', 'Duration [hrs]']].groupby(['Subject', 'Semester'], as_index=False).sum()
    ret_df.sort_values(by='Duration [hrs]', ascending=False, inplace=True)
    return ret_df


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
ects = pd.read_csv("data/ects.csv")

# transform the dataset
df = transform_datasets(winter_df, summer_df)

expected_and_realized_dur_per_subj_df = compute_expected_duration_per_subject(df, ects)
total_dur_per_subj_df = compute_total_duration_per_subject(df)