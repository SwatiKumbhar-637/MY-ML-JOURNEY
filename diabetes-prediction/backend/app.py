from flask import Flask
from flask_cors import CORS

from routes.prediction import prediction_bp


app = Flask(__name__)

CORS(app)

app.register_blueprint(prediction_bp)


@app.route("/")
def home():
    return "Diabetes Prediction API is running!"


if __name__ == "__main__":
    app.run(debug=True)