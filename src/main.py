from data_loader import load_data, get_X
from train_models import train_party_model

parties = ["S", "M", "L", "C", "KD", "V", "MP", "SD"]

files = {
    'CPI': 'consumer_price_index.csv',
    'EC': 'electricity_consumption.csv',
    'GD': 'government_debt.csv',
    'MSR': 'money_supply_growth.csv',
    'MIR': 'mortgage_interest_rate.csv',
    'Pop': 'population_00-24.csv',
    'UR': 'unemployment_rate.csv'
    }


def main():
    df = load_data(files)
    X = get_X(df)
    models = train_party_model(df, X, parties)
    print("Models trained and saved!")
    

if __name__ == "__main__":
    main()