import pandas as pd
from functools import reduce

parties = ["S", "M", "L", "C", "KD", "V", "MP", "SD"]

def load_data(files: map) -> pd.DataFrame:
    """Load and merge multiple CSV files into a single DataFrame, including party polling data.

    Parameters
    ----------
    files : dict
        Dictionary mapping feature names to their corresponding CSV filenames.

    Returns
    -------
    df : pandas.DataFrame
        Merged DataFrame containing all features and party polling columns, 
        with rows before September 2006 removed and the 'date' column dropped.
    """
    
    dfs = []
    
    for col_name, file in files.items():
        df = pd.read_csv(f'data/raw_data/{file}')
        
        dfs.append(df)

    df = reduce(
        lambda left, right: pd.merge(left, right, on="date", how="inner"),
        dfs
    )

    sentiment = pd.read_csv('data/raw_data/polls.csv')
    df = df.merge(sentiment, on='date', how='inner')
    
    df = df[df['date'] >= '2006-09']

    df = df.drop('date', axis =1)
    
    return df

def get_X(df):
    """
    Extract feature columns (X) from the full dataset by removing party polling columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Full dataset including features and party polling columns.

    Returns
    -------
    X : pandas.DataFrame
        DataFrame containing only feature columns for model training or prediction.
    """
    
    parties = ["S", "M", "L", "C", "KD", "V", "MP", "SD"]
    X = df.drop(columns =parties)
    return X
