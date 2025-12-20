import pandas as pd


URL = "https://raw.githubusercontent.com/MansMeg/SwedishPolls/master/Data/Polls.csv"

def fetch_poll_data() -> pd.DataFrame:
    """
    Fetch poll data from the predefined URL and return it as a pandas DataFrame.

    Args:
        url (str): URL pointing to the poll data source.

    Returns:
        pd.DataFrame: DataFrame containing the fetched poll data.
    """
    df = pd.read_csv(URL)
    
    return df


def filter_poll_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the poll data DataFrame by only keeping the poll data from Sifo for each party and the
    time of the measurement. 

    Args:
        df (pd.DataFrame): Raw poll data DataFrame.

    Returns:
        pd.DataFrame: Filtered poll data DataFrame.
    """
    
    filtered_df = df.copy()
    filtered_df = filtered_df[filtered_df["Company"] == "Sifo"] 
    
    cols = [
    "PublYearMonth",
    "M", "L", "C", "KD", "S", "V", "MP", "SD"
    ]
    filtered_df = filtered_df[cols]
    
    return filtered_df


def process_poll_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts YearMonth column from YYYY-mon to YYYY-MM format and renames column
    from "PublYearMonth" to "date".

    Args:
        df (pd.DataFrame): Filtered poll data DataFrame

    Returns:
        pd.DataFrame: Processed poll data DataFrame
    """
    
    processed_df = df.copy()
    
    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "maj": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "okt": "10", "nov": "11", "dec": "12"
    }

    s = processed_df["PublYearMonth"].astype(str).str.strip().str.lower()
    year = s.str.slice(0, 4)
    month = s.str.slice(5).map(month_map)
    
    processed_df["PublYearMonth"] = pd.PeriodIndex(year + "-" + month, freq="M")
    processed_df = processed_df.rename(columns={"PublYearMonth": "date"})
    
    return processed_df


if __name__ == "__main__":
    data = fetch_poll_data()
    filtered_data = filter_poll_data(data)
    processed_data = process_poll_data(filtered_data)
    
    #Create CSV-file
    processed_data.to_csv("raw_data/polls.csv", index=False)