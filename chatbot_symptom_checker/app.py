from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from main import final_ouput
app = Flask(__name__)
CORS(app)

# Load the dataset
data = pd.read_csv('Diseases_Symptoms.csv')  # Replace with the correct path if needed

# Prepare the data for training
X = data['Symptoms']
y = data['Name']
treatments = data[['Name', 'Treatments']]

# Convert text data to numerical features
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Function to predict the condition and provide treatments
def find_condition_and_treatment(user_input):
    # Convert the user input to the same format as the training data
    user_input_vectorized = vectorizer.transform([user_input])
    
    # Predict the condition
    predicted_condition = model.predict(user_input_vectorized)[0]
    
    # Find the treatments for the predicted condition
    treatments_for_condition = treatments.loc[treatments['Name'] == predicted_condition, 'Treatments'].values[0]
    
    return predicted_condition, treatments_for_condition

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    # Use the machine learning model to find condition and treatment
    predicted_condition, treatment = final_ouput(user_message)
    
    # Create the response message
    response_message = f"Based on the symptoms you provided, the possible condition is: {predicted_condition}. Recommended treatments are: {treatment}."
    
    return jsonify({"message": response_message})

if __name__ == "__main__":
    app.run(debug=True)
