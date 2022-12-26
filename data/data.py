import pandas as pd


def transform_datasets(_winter_df: pd.DataFrame, _summer_df: pd.DataFrame) -> pd.DataFrame:
    _winter_df['Semester'] = 'W'
    _summer_df['Semester'] = 'S'
    _df = pd.concat([_winter_df, _summer_df], axis=0)

    _df['Start'] = pd.to_datetime(_df['Date'] + " " + _df['Start'])
    _df['End'] = pd.to_datetime(_df['Date'] + " " + _df['End'])
    _df.insert(3, 'Duration [hrs]', (_df['End'] - _df['Start']) / pd.Timedelta(hours=1))
    return _df


def get_total_duration_per_subject(_df: pd.DataFrame, _ects: pd.DataFrame) -> pd.DataFrame:
    _dur_df = _df[['Subject', 'Duration [hrs]']].groupby(['Subject']).sum()
    _dur_df = _dur_df.join(other=_ects.set_index('Subject'), how='inner')
    _dur_df = _dur_df.sort_values(by=['ECTS', 'Duration [hrs]'], ascending=False)

    _dur_df['Min exp duration [hrs]'] = _dur_df['ECTS'] * 25
    _dur_df['Max exp duration [hrs]'] = _dur_df['ECTS'] * 30
    return _dur_df
