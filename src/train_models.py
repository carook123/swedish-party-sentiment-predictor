import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
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
    metrics = {}

    r2_scores = []
    mse_scores = []
    
    for party in parties:
        y_party = df[party]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y_party, random_state=42, test_size=0.2)

        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)  
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        metrics[party] = {
            "mse": mse,
            "r2": r2
        }

        r2_scores.append(r2)
        mse_scores.append(mse)

        models[party] = model
        
        joblib.dump(model, f"models/rf_{party}.joblib")

    metrics["average"] = {
        "mse": float(sum(mse_scores) / len(mse_scores)),
        "r2": float(sum(r2_scores) / len(r2_scores))
    }
    
    joblib.dump(metrics, "models/model_metrics.joblib")

    return models

