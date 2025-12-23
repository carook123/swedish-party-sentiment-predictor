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
### 1. Installation
Initially, clone the repository by running the following command from a directory of your choice:

```bash
git clone https://github.com/carook123/swedish-party-sentiment-predictor.git
```

Moving on, make sure you have Python 3.9+ installed. The project relies on standard data science libraries found in requirements.txt. Install these in your chosen environment using.

```bash
pip install -r requirements.txt
```

### 2. Project structure
Before running the project, ensure the following directory structure exists:

```bash
project-root/
│
├── app.py
├── models/          
├── src/
│   ├── main.py
│   ├── data_loader.py
│   ├── train_models.py
│   └── predict_sentiment.py
└── data/
    └── raw_data/
```
The `models/` directory already contains trained models, so you do not need to train them before running the application.

### 3. Launch the application

From the project root, start the Dash app:
```bash
python app.py
```

This will launch a local web server.
Once the app is running, users can input values for the economic indicators and receive predicted polling sentiment for all Swedish political parties.

### 4. (Optional) Retrain the models
If you want to retrain the models yourself (for example, using updated data or different parameters), you can do so from the project root by running the main script:
```bash
python src/main.py
```
This will:
1. Load and merge the raw data files
2. Clean and format the dataset
3. Train one Random Forest regression model per political party
4. Overwrite the existing `.joblib` files inside the `models/` directory

After retraining, the application will automatically use the newly trained models.

## Authors
* [Carolina Oker-Blom](https://github.com/carook123)
* [Albin Kårlin](https://github.com/albinkaarlin)
* [Sofie Melander](https://github.com/sofiemelander)
