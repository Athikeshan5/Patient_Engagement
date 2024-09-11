import pandas as pd
import re
from fuzzywuzzy import process  # For fuzzy string matching
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load the symptom dataset
file_path = 'Book2.xlsx'  # Replace with the correct path
df = pd.read_excel(file_path)
all_symptoms = df['Symptoms'].tolist()

def extract_symptoms(user_input, symptoms_list):
    matched_symptoms = set()
    user_input = user_input.lower()
    user_input = re.sub(r'[^\w\s,]', '', user_input)
    input_symptoms = [symptom.strip() for symptom in re.split(r',|\s+', user_input) if symptom.strip()]
    for input_symptom in input_symptoms:
        closest_match = process.extractOne(input_symptom, symptoms_list)
        if closest_match and closest_match[1] > 70:
            matched_symptoms.add(closest_match[0].capitalize())
    return matched_symptoms

# Load the disease and symptoms dataset
data = pd.read_csv('Diseases_Symptoms.csv')  # Replace with your actual file name
X = data['Symptoms']
y = data['Name']
treatments = data[['Name', 'Treatments']]

# Prepare the vectorizer and model
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

def find_condition_and_treatment(user_input):
    user_input_vectorized = vectorizer.transform([user_input])
    predicted_condition = model.predict(user_input_vectorized)[0]
    treatments_for_condition = treatments.loc[treatments['Name'] == predicted_condition, 'Treatments'].values[0]
    return predicted_condition, treatments_for_condition

def final_ouput(user_input):
    # Step 1: Extract symptoms from user input
    extracted_symptoms = extract_symptoms(user_input, all_symptoms)
    
    # Convert the extracted symptoms into a comma-separated string
    formatted_input = ', '.join(extracted_symptoms)
    
    # Step 2: Find the condition and treatment based on extracted symptoms
    predicted_condition, treatments = find_condition_and_treatment(formatted_input)
    
    return predicted_condition, treatments

