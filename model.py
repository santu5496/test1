import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import accuracy_score
import random

class DisasterPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
        self.data = None
        self.model_filename = "disaster_model.pkl"
        self.X = None
        self.y = None

    def _generate_random_data(self, num_samples=1000):
        data = []
        for _ in range(num_samples):
            temperature = random.uniform(20, 45)
            rainfall = random.uniform(0, 200)
            wind_speed = random.uniform(0, 100)
            humidity = random.uniform(30, 100)

            if temperature > 35 and humidity > 60:
                disaster_type = "Heat Wave"
            elif wind_speed > 60 and humidity > 80:
                disaster_type = "Cyclone/Storm"
            elif rainfall > 100:
                disaster_type = "Flood"
            else:
                disaster_type = "No immediate disaster"
            
            data.append([temperature, rainfall, wind_speed, humidity, disaster_type])

        df = pd.DataFrame(data, columns=['temperature', 'rainfall', 'wind_speed', 'humidity', 'disaster_type'])
        return df

    def save_model(self):
        joblib.dump(self.model, self.model_filename)

    def load_model(self):
        try:
            self.model = joblib.load(self.model_filename)
        except FileNotFoundError:
            self.train()
    def train(self):
        self.data = self._generate_random_data()
        self.X = self.data[['temperature', 'rainfall', 'wind_speed', 'humidity']]
        self.y = self.data['disaster_type']
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        self.save_model()
        print(f"Model accuracy: {accuracy}")
        
    def predict(self, input_data):
        if self.model is None or self.data is None:
            raise Exception("Model not trained yet. Call the 'train' method first.")
        input_df = pd.DataFrame([input_data], columns=['temperature', 'rainfall', 'wind_speed', 'humidity'])
        prediction = self.model.predict(input_df)
        return prediction[0]