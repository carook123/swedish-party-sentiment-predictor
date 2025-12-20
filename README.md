# Swedish Party Sentiment Predictor
This project attempts to predict Swedish opinion polls based on socially relevant metrics using the classic statistical models Random Forest and Linear Regression.  

This project is the authors' submission to the final project assignment of [LINC-STEM](https://linclund.com/committees/stem/)'s Advanced Python Workshop of autumn 2025. 

## Data sources and explanation
All socially relevant metrics are retrieved from swedish statistical authority [SCB](https://www.scb.se/) using their public API:s. Below is a table explaining each metric.  

| Metric | Description |
|----------|----------|
| CPI (Consumer Price Index)      | A measure of swedish inflation that tracks changes over time in the price level of a fixed basket of consumer goods and services.        |
| GD (Government Debt)       | The total outstanding debt of the swedish government across all financial markets, reflecting public sector borrowing.        |
|UR (Unemployment Rate) |The share of the labor force aged 15–74 that is unemployed, based on survey data and not adjusted for seasonal effects.|
|MSR (Money Supply Growth, 12-month rate)|The annual growth rate of the money supply, indicating changes in liquidity and monetary conditions in the economy.
|MIR (Mortgage Interest Rate)|The average interest rate applied to new or outstanding mortgage loans, reflecting household borrowing costs.|
|EC (Electricity Consumption)|The total amount of electricity consumed over a given period, often used as a proxy for economic activity.|
|Pop (Population)|Annual total population figures covering the period 2000–2024, used for demographic trends and normalization.|

The Swedish poll data is retrieved from the repository [Swedish Polls](https://github.com/MansMeg/SwedishPolls) which gathers data from all major swedish poll frequently. A special thanks to everyone who has contributed to this repo. We have chosen to only include data for the political parties currently part of the swedish parliament - these are:

|Party abbreviation|Party name|
|-|-|
|M|Moderate Party|
|L|Liberal Party|
|C|Centre Party|
|KD|Christian Democrats|
|S|Social Democrats|
|V|Left Party|
|MP|Green Party|
|SD|Sweden Democrats|

## How to run

## Authors
* [Carolina Oker-Blom](https://github.com/carook123)
* [Albin Kårlin](https://github.com/albinkaarlin)
* [Sofie Melander](https://github.com/sofiemelander)