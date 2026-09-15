Car Price Prediction

A machine learning project that predicts the resale price of used cars based on company, fuel type, car age, and kilometers driven.

Tech Stack

Python
Pandas
Scikit-learn
Joblib
Flask
React
CSS

Machine Learning Workflow

Data Cleaning
↓
EDA
↓
Feature Engineering
↓
Preprocessing
↓
Model Training
↓
Hyperparameter Tuning
↓
Model Evaluation
↓
Model Saving
↓
Flask API
↓
React Frontend

Dataset

The project uses the Quikr Car Dataset.

The data is cleaned and preprocessed before training the models.

Features Used

Company
Fuel Type
Car Age
Kilometers Driven

Target

Car Price

Models Used
Linear Regression
Random Forest Regression
Tuned Random Forest Regression
Model Performance
Model	MAE	RMSE	R²
Linear Regression	₹154,872	₹292,278	0.4773
Random Forest	₹129,361	₹263,113	0.5764
Tuned Random Forest	₹131,319	₹262,830	0.5774

The Tuned Random Forest achieved the highest R² score of 0.5774.

Preprocessing

Numerical and categorical features are handled using a Scikit-learn preprocessing pipeline.

Categorical features such as company and fuel_type are converted using One-Hot Encoding.

Hyperparameter Tuning

GridSearchCV with 5-fold cross-validation was used to tune the Random Forest model.

Parameters tested:

n_estimators
max_depth
min_samples_split
min_samples_leaf

Feature Importance
Feature	Importance
Company	43.48%
Kilometers Driven	29.34%
Car Age	23.62%
Fuel Type	3.57%
Application

The project includes a Flask backend and React frontend.

Prediction

Users can enter car details and select a machine learning model to get an estimated resale price.

Evaluation

A separate evaluation page displays model performance metrics and feature importance dynamically from the backend.

API
GET /options

Returns available companies, fuel types, and prediction models.

POST /predict

Accepts car details and returns the predicted price.

Project Structure

car-price-prediction/

├── data/
├── models/
├── notebooks/
├── src/
├── backend/
├── frontend/
├── requirements.txt
└── README.md

How to Run
Backend

cd backend

python -m app.app

The Flask API runs on:

http://127.0.0.1:5000

Frontend

cd frontend

npm install

npm run dev

What I Learned

This project helped me understand the complete machine learning workflow, from data cleaning and EDA to model training, evaluation, hyperparameter tuning, model saving, API development, and React frontend integration.

Disclaimer

This project is created for learning purposes. The predicted prices are estimates based on the available dataset.

After pasting, press Ctrl + S.

Then open the Preview of README.md in VS Code (Ctrl + Shift + V). You should see the properly formatted GitHub-style README instead of the raw Markdown.