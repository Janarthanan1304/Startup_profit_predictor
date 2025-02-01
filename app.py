
from flask import Flask, request, jsonify, render_template, send_from_directory
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('startup_data.csv')

# Define the features (X) and target variable (y)
X = df[['R&D Spend', 'Administration', 'Marketing Spend', 'state']]
y = df['Profit']

# One-hot encode the state
X = pd.get_dummies(X, columns=['state'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model on the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Define a function to make predictions based on user input
def make_prediction(RD_Spend, Administration, Marketing_Spend, state):
    # Create a DataFrame with the user input
    user_input = pd.DataFrame({'R&D Spend': [RD_Spend], 'Administration': [Administration], 'Marketing Spend': [Marketing_Spend]})

    # One-hot encode the state
    state_one_hot = pd.get_dummies(pd.Series([state]), prefix='state')
    user_input = pd.concat([user_input, state_one_hot], axis=1)

    # Add missing columns
    missing_columns = ['state_California', 'state_Florida', 'state_New York']
    for column in missing_columns:
        if column not in user_input.columns:
            user_input[column] = 0

    # Reorder the columns to match the training data
    user_input = user_input[X.columns]

    # Make a prediction using the trained model
    prediction = model.predict(user_input)
    return prediction[0]

# Define a route to handle POST requests from the index.html file
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        RD_Spend = float(data['R&D Spend'])
        Administration = float(data['Administration'])
        Marketing_Spend = float(data['Marketing Spend'])
        state = data['state']
        predicted_profit = make_prediction(RD_Spend, Administration, Marketing_Spend, state)
        return jsonify({'predicted_profit': predicted_profit})
    except Exception as e:
        app.logger.error(f'Error making prediction: {e}')
        return jsonify({'error': 'Error making prediction'}), 500

# Define a route to handle GET requests to the root URL
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
