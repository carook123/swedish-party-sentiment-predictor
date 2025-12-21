import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd


def train_party_model(df: pd.DataFrame, X: pd.DataFrame, parties: list) -> dict:
    """Train a separate Random Forest regression model for each political party 
    using macroeconomic and demographic features.

    Each model is trained to predict the monthly polling percentage for 
    the corresponding party. The trained models are saved to disk in the 
    'models' directory as 'rf_<party>.joblib'.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The full dataset including features and target party columns.
    X : pandas.DataFrame
        DataFrame containing the feature columns used for prediction.
    parties : list of str
        List of party column names in `df` to train separate models for.
    
    Returns
    -------
    models : dict
        Dictionary where keys are party names and values are the trained 
        RandomForestRegressor models.
        
    Notes
    -----
    - Ensure that a 'models' directory exists at the path '../models/' 
      before running this function.
    - Run this function from the main project directory (one level above 'models').
    """
    
    models = {}
    
    for party in parties:
        y_party = df[party]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y_party, random_state=42, test_size=0.2)

        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)  
        model.fit(X_train, y_train)
        
        #y_pred = model.predict(X_test)

        models[party] = model
        
        joblib.dump(model, f"../models/rf_{party}.joblib")

    return models

