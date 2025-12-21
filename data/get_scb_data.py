import requests
import pandas as pd
import json

def fetch_scb_data(url, name, filename, query, aggregate):

    r = requests.post(url, json=query)
    r.raise_for_status()
    data = r.json()["data"]

    df = pd.DataFrame([
        {"date": d["key"][-1], name: float(d["values"][0])}
        for d in data
    ])
    
    #Matching date-format (YYYY-MM) for all data
    df["date"] = (
        df["date"]
        .astype(str)
        .str.replace("M", "-", regex=False)
        .pipe(pd.PeriodIndex, freq="M")
        .astype(str)
    )

    if aggregate: # Summera om samma månad förekommer flera gånger
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


# All metrics and their query

for metric in metrics:
    fetch_scb_data(
        url=metric["url"],
        name=metric["name"],
        filename=metric["filename"],
        query=metric["query"],
        aggregate= metric["aggregate"]
    )

# KPI - fastställda tal
# Statsskuld - total alla markander
# Arbetslöshet AKU - procent, Icke säsongrensad, Total män och kvinnor, Totalt 15-74 år	
# Pänningmängd - Tillväxttakt 12-månaders, procent efter penningmängdsmått och månad
# Bolåneränta (nyckeltal) - genomsnitt, procentssats
# Elanvändning - summa förburkad el
# Befolkning1 - totalt år 2025
# Befolkning2 - totalt år 2000-2024
