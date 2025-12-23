import requests
import pandas as pd
import json

def fetch_scb_data(url, name, filename, query, aggregate):
    """
    Fetches time series data from SCB API using a POST request and converts
    the response to a pandas DataFrame with a standardized YYYY-MM date format.

    If multiple entries exist for the same month and aggregation is enabled,
    values are summed per month. The resulting DataFrame is sorted in
    chronological order and saved as a CSV file.
    """

    r = requests.post(url, json=query)
    r.raise_for_status()
    data = r.json()["data"]

    df = pd.DataFrame([
        {"date": d["key"][-1], name: float(d["values"][0])}
        for d in data
    ])
    
    # Matching date-format (YYYY-MM) for all data
    df["date"] = (
        df["date"]
        .astype(str)
        .str.replace("M", "-", regex=False)
        .pipe(pd.PeriodIndex, freq="M")
        .astype(str)
    )

    if aggregate: 
        df = (
            df
            .groupby("date", as_index=False)
            .sum()
            .rename(columns={"value": name})
        )

    df = df.iloc[::-1].reset_index(drop=True)

    df.to_csv(f"data/raw_data/{filename}", index=False)
    print(f"Saved {filename}")

metrics = []
with open("data/scb_metrics.json", "r", encoding="utf-8") as f:
    metrics = json.load(f)

for metric in metrics:
    fetch_scb_data(
        url=metric["url"],
        name=metric["name"],
        filename=metric["filename"],
        query=metric["query"],
        aggregate= metric["aggregate"]
    )

# Combining population 00-24 and population 25 into one csv file
population = pd.concat([pd.read_csv("data/raw_data/population_25.csv"), pd.read_csv("data/raw_data/population_00-24.csv")], ignore_index=True)
population.to_csv("data/raw_data/population_00-25.csv", index=False)
