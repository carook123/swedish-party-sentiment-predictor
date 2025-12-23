import joblib
import pandas as pd

parties = ["S", "M", "L", "C", "KD", "V", "MP", "SD"]

models = {party: joblib.load(f"models/rf_{party}.joblib") for party in parties}

def predict_sentiment(user_input: dict) -> dict:
    """Predict party polling percentages using pre-trained Random Forest models.

    Parameters
    ----------
    user_input : dict
        Dictionary containing feature values for prediction, 
        where keys match the columns used for training.

    Returns
    -------
    predictions : dict
        Dictionary mapping each party name to its predicted polling percentage.

    Notes
    -----
    - Expects pre-trained models saved as 'models/rf_<party>.joblib' 
      for each party.
    """
    
    X = pd.DataFrame([user_input])
    #predictions = {}
    predictions = {party: float(models[party].predict(X)[0]) for party in parties}

    #for party in parties:
    #    model = joblib.load(f"models/rf_{party}.joblib")
    #    predictions[party] = float(model.predict(X)[0])
        
    return predictions