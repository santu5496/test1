import random
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class DisasterPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
        self.model_filename = "disaster_model.pkl"

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
        data = self._generate_random_data()
        X = data[['temperature', 'rainfall', 'wind_speed', 'humidity']]
        y = data['disaster_type']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, self.model.predict(X_test))
        self.save_model()
        print(f"Model trained with accuracy: {accuracy}")

    def predict(self, input_data):
        input_df = pd.DataFrame([input_data], columns=['temperature', 'rainfall', 'wind_speed', 'humidity'])
        prediction = self.model.predict(input_df)[0]
        class_index = list(self.model.classes_).index(prediction)
        probability = self.model.predict_proba(input_df)[0][class_index]
        will_occur = "Yes" if probability > 0.5 else "No"
        return prediction, probability, will_occur
