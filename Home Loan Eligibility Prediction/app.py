from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd

app = Flask(__name__)

# Load the model
with open('loan_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Function to preprocess input data
def preprocess_input(data):
    # Convert numeric fields to appropriate types
    data['ApplicantIncome'] = data['ApplicantIncome'].astype(float)
    data['CoapplicantIncome'] = data['CoapplicantIncome'].astype(float)
    data['LoanAmount'] = data['LoanAmount'].astype(float)
    data['Loan_Amount_Term'] = data['Loan_Amount_Term'].astype(float)
    data['Credit_History'] = data['Credit_History'].astype(float)

    # Convert categorical fields to boolean where applicable
    data['Gender'] = data['Gender'].apply(lambda x: 1 if x == 'Male' else 0)
    data['Married'] = data['Married'].apply(lambda x: 1 if x == 'Yes' else 0)
    data['Education'] = data['Education'].apply(lambda x: 1 if x == 'Graduate' else 0)
    data['Self_Employed'] = data['Self_Employed'].apply(lambda x: 1 if x == 'Yes' else 0)

    # Handle Dependents
    data = pd.concat([data, pd.get_dummies(data['Dependents'], prefix='Dependents')], axis=1)
    
    # Ensure all expected dummy columns are present
    for col in ['Dependents_0', 'Dependents_1', 'Dependents_2', 'Dependents_3+']:
        if col not in data.columns:
            data[col] = 0

    # Handle Property_Area
    data = pd.concat([data, pd.get_dummies(data['Property_Area'], prefix='Property_Area')], axis=1)
    
    # Ensure all expected dummy columns are present
    for col in ['Property_Area_Rural', 'Property_Area_Semiurban', 'Property_Area_Urban']:
        if col not in data.columns:
            data[col] = 0

    # Drop the original categorical columns
    columns_to_drop = ['Dependents', 'Property_Area']
    data.drop(columns=columns_to_drop, inplace=True)

    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()

    input_data = pd.DataFrame([data])

    input_data = preprocess_input(input_data)

    prediction = model.predict(input_data)[0]

    prediction_text = "Congratulations! Your loan is eligible." if prediction == 1 else "Sorry, your loan is not eligible."

    return redirect(url_for('show_result', prediction_text='Loan Status: {}'.format(prediction_text)))

@app.route('/result')
def show_result():
    prediction_text = request.args.get('prediction_text', '')
    return render_template('result.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)
