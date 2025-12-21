import pandas as pd
import numpy as np 

URL = "https://raw.githubusercontent.com/MansMeg/SwedishPolls/master/Data/Polls.csv"
party_cols = ["M", "L", "C", "KD", "S", "V", "MP", "SD"]


def convert_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts YearMonth column from YYYY-mon to YYYY-MM format
    and renames column from "PublYearMonth" to "date".
    """
    
    new_df = df.copy()
    
    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "maj": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "okt": "10", "nov": "11", "dec": "12"
    }

    s = new_df["PublYearMonth"].astype(str).str.strip().str.lower()
    year = s.str.slice(0, 4)
    month = s.str.slice(5).map(month_map)
    
    new_df["PublYearMonth"] = pd.PeriodIndex(year + "-" + month, freq="M")
    new_df = new_df.rename(columns={"PublYearMonth": "date"})
    
    return new_df


def drop_excess_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop all columns except for date, party columns and sample size.
    """
    
    filtered_df = df.copy()
    
    cols = ["date","n"] + party_cols
    filtered_df = filtered_df[cols]
    
    return filtered_df


def monthly_weighted_average(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group each data-row by year and month, if group is larger than 1 take
    the weighted average from the sample size. If no sample size exists,
    take mean value of other sample sizes in same group.
    """

    new_df = df.copy()
    
    #Global sample size in case all rows in a group lacks n
    global_mean_n = new_df["n"].mean()

    # Fill missing n per month with that month's mean n
    new_df["n"] = new_df.groupby("date")["n"].transform(lambda s: s.fillna(s.mean()))
    # If still missing use global mean
    new_df["n"] = new_df["n"].fillna(global_mean_n).astype(float)

    # Weighted average per party within each month
    out = pd.DataFrame(index=new_df.groupby("date").size().index)

    for c in party_cols:
        x = new_df[c]
        w = new_df["n"]

        # Use weights only where x exists; if x is NaN, weight = 0 
        w_used = w.where(x.notna(), 0.0)

        weighted_sum = (x.fillna(0.0) * w_used).groupby(new_df["date"]).sum()
        weight_sum = w_used.groupby(new_df["date"]).sum()

        out[c] = weighted_sum / weight_sum.replace(0, pd.NA)

    #Include date column and sort newest measurement first
    out = out.sort_index(ascending=False)
    out = out.reset_index() 
    
    return out


def linear_interpolation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values via linear interpolation per party column,
    but only within the range of existing data for that party. Keep NaN values.
    """
    new_df = df.copy()

    # Make sure columns are numeric but keep NaN
    new_df[party_cols] = new_df[party_cols].apply(pd.to_numeric, errors="coerce")

    # Sort by old for interpolation
    new_df = new_df.set_index("date").sort_index()

    # Calculate full monthly range
    full_range = pd.period_range(new_df.index.min(), new_df.index.max(), freq="M")
    new_df = new_df.reindex(full_range)
    new_df.index.name = "date"

    # Interpolate each column, but only within existing data range
    for col in party_cols:
        s = new_df[col]

        first = s.first_valid_index()
        last = s.last_valid_index()


        # Interpolate only in the middle range
        s_mid = s.loc[first:last].interpolate(method="linear")

        # Write back segment outside remains NaN
        new_df.loc[first:last, col] = s_mid

    # Newest measure first again
    new_df = (
        new_df.reset_index()
              .sort_values("date", ascending=False)
              .reset_index(drop=True)
    )

    return new_df



def normalize_percentages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Round every poll measure to one decimal and make sure all sum up to 100.0
    per month. Keep NaN values.
    """
    new_df = df.copy()

    # Make sure columns are numeric. Keep NaN.
    new_df[party_cols] = new_df[party_cols].apply(pd.to_numeric, errors="coerce")

    for i in range(len(new_df)):
        row = new_df.loc[i, party_cols] # type: ignore

        # Parties that "exist" this month
        mask = row.notna()
        if mask.sum() == 0:
            continue

        # Force numeric values
        values = pd.to_numeric(row[mask], errors="coerce").astype("float64")

        total = float(values.sum())
        if total == 0.0 or np.isnan(total):
            continue

        # Scale to 100
        scaled = values * (100.0 / total)

        # Round to 1 decimal
        rounded = scaled.round(1)

        # Fix rounding errors to make sum exactly 100.0
        diff = round(100.0 - float(rounded.sum()), 1)
        if diff != 0.0:
            col_to_adjust = rounded.idxmax()
            rounded[col_to_adjust] = round(float(rounded[col_to_adjust]) + diff, 1)

        # Write back, NaN remains
        new_df.loc[i, rounded.index] = rounded

    return new_df


if __name__ == "__main__":
    
    data = pd.read_csv(URL)
    
    data = convert_date(data)
    data = drop_excess_columns(data)
    data = monthly_weighted_average(data)
    data = linear_interpolation(data)
    data = normalize_percentages(data)
    
    data.to_csv("data/raw_data/polls.csv", index=False, na_rep="NA")