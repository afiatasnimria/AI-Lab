import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

data = {
    'Hours_Studied': [2.0, 3.5, 5.0, 1.0, 4.0, 6.0, 1.5, 3.0, 2.5, 4.5],
    'Hours_Slept': [7.0, 6.0, 8.0, 5.0, 6.5, 8.5, 6.0, 7.0, 5.0, 7.5],
    'Prior_Grade': [70, 65, 80, 50, 78, 85, 60, 75, 55, 82],
    'Result': ['fail', 'fail', 'pass', 'fail', 'pass', 'pass', 'fail', 'pass', 'fail', 'pass']
}


df = pd.DataFrame(data)

print("First few rows of the dataset:")
print(df.head())
print("\nDataset Description:")
print(df.describe())
print("\nVariables:")
print("Hours_Studied: Number of hours the student studies per day.")
print("Hours_Slept: Number of hours the student sleeps per day.")
print("Prior_Grade: Average grade before the exam.")
print("Result: Pass/Fail label for the exam.")


print("\nMissing values:")
print(df.isnull().sum())

df['Result'] = df['Result'].map({'fail': 0, 'pass': 1})


scaler = StandardScaler()
features = ['Hours_Studied', 'Hours_Slept', 'Prior_Grade']
df[features] = scaler.fit_transform(df[features])


X = df[features]
y = df['Result']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


k = 3  
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)


y_pred = knn.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"\nAccuracy: {accuracy}")
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(class_report)


example = [[3, 6.5, 77]]
example_scaled = scaler.transform(example)
prediction = knn.predict(example_scaled)
print(f"\nPrediction for input {example}: {'pass' if prediction[0] == 1 else 'fail'}")
