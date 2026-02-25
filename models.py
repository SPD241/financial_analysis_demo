import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class Model_creation:
    def __init__(self, data):
        self.data = data
        self.scaler = StandardScaler()

    def preprocess_data(self):
        features = self.data.drop('Close', axis=1)
        target = self.data['Close']
        
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=0)
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test