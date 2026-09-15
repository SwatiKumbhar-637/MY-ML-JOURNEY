import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Evaluation() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  // =========================================================
  // LOAD EVALUATION DATA FROM FLASK
  // =========================================================

  useEffect(() => {
    fetch("http://127.0.0.1:5000/evaluation")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load evaluation data");
        }

        return response.json();
      })
      .then((result) => {
        console.log("Evaluation data:", result);

        if (!result.success) {
          throw new Error(
            result.error || "Failed to load evaluation"
          );
        }

        setData(result);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
      });
  }, []);

  // =========================================================
  // LOADING
  // =========================================================

  if (!data && !error) {
    return (
      <div className="app">
        <nav className="navbar">
          <div className="logo">
            Car Price Predictor
          </div>

          <div className="nav-links">
            <Link to="/">
              Prediction
            </Link>

            <Link
              to="/evaluation"
              className="active"
            >
              Evaluation
            </Link>
          </div>
        </nav>

        <main className="main-container">
          <div className="page-header">
            <h1>Model Evaluation</h1>

            <p>
              Loading evaluation results...
            </p>
          </div>
        </main>
      </div>
    );
  }

  // =========================================================
  // ERROR
  // =========================================================

  if (error) {
    return (
      <div className="app">
        <nav className="navbar">
          <div className="logo">
            Car Price Predictor
          </div>

          <div className="nav-links">
            <Link to="/">
              Prediction
            </Link>

            <Link
              to="/evaluation"
              className="active"
            >
              Evaluation
            </Link>
          </div>
        </nav>

        <main className="main-container">
          <div className="page-header">
            <h1>Model Evaluation</h1>

            <div className="error-message">
              {error}
            </div>
          </div>
        </main>
      </div>
    );
  }

  // =========================================================
  // GROUP FEATURE IMPORTANCE
  // =========================================================

  const groupedImportance = {};

  data.feature_importance.forEach((item) => {
    let featureName = item.feature;

    if (featureName.includes("car_age")) {
      featureName = "Car Age";
    } else if (featureName.includes("kms_driven")) {
      featureName = "Kilometers Driven";
    } else if (featureName.includes("company")) {
      featureName = "Company";
    } else if (featureName.includes("fuel_type")) {
      featureName = "Fuel Type";
    }

    if (!groupedImportance[featureName]) {
      groupedImportance[featureName] = 0;
    }

    groupedImportance[featureName] += item.importance;
  });

  // =========================================================
  // SORT FEATURE IMPORTANCE
  // =========================================================

  const featureImportanceList = Object.entries(
    groupedImportance
  ).sort((a, b) => b[1] - a[1]);

  // =========================================================
  // FORMAT MODEL NAME
  // =========================================================

  const formatModelName = (name) => {
    return name
      .replaceAll("_", " ")
      .replace(/\b\w/g, (char) =>
        char.toUpperCase()
      );
  };

  // =========================================================
  // FORMAT CURRENCY
  // =========================================================

  const formatCurrency = (value) => {
    return `₹${Number(value).toLocaleString(
      "en-IN",
      {
        maximumFractionDigits: 2,
      }
    )}`;
  };

  // =========================================================
  // UI
  // =========================================================

  return (
    <div className="app">

      {/* =====================================================
          NAVBAR
      ===================================================== */}

      <nav className="navbar">

        <div className="logo">
          Car Price Predictor
        </div>

        <div className="nav-links">

          <Link to="/">
            Prediction
          </Link>

          <Link
            to="/evaluation"
            className="active"
          >
            Evaluation
          </Link>

        </div>

      </nav>


      {/* =====================================================
          MAIN CONTENT
      ===================================================== */}

      <main className="main-container">

        <div className="page-header">

          <h1>
            Model Evaluation
          </h1>

          <p>
            Compare the performance of the trained models.
          </p>

        </div>


        {/* ===================================================
            MODEL PERFORMANCE
        =================================================== */}

        <section>

          <div className="section-heading">

            <h2>
              Model Performance
            </h2>

            <p>
              Lower MAE and RMSE are better, while a higher R² score indicates better performance.
            </p>

          </div>


          <div className="model-grid">

            {Object.entries(data.models).map(
              ([modelName, metrics]) => (

                <div
                  className="model-card"
                  key={modelName}
                >

                  <h3>
                    {formatModelName(modelName)}
                  </h3>


                  <div className="metric">

                    <span>
                      MAE
                    </span>

                    <strong>
                      {formatCurrency(metrics.mae)}
                    </strong>

                  </div>


                  <div className="metric">

                    <span>
                      RMSE
                    </span>

                    <strong>
                      {formatCurrency(metrics.rmse)}
                    </strong>

                  </div>


                  <div className="metric">

                    <span>
                      R² Score
                    </span>

                    <strong className="r2-value">
                      {Number(metrics.r2).toFixed(4)}
                    </strong>

                  </div>

                </div>

              )
            )}

          </div>

        </section>


        {/* ===================================================
            FEATURE IMPORTANCE
        =================================================== */}

        <section className="feature-section">

          <div className="section-heading">

            <h2>
              Feature Importance
            </h2>

            <p>
              Relative contribution of each input feature to the Random Forest model.
            </p>

          </div>


          <div className="feature-list">

            {featureImportanceList.map(
              ([feature, importance]) => {

                const percentage =
                  importance * 100;

                return (

                  <div
                    className="feature-row"
                    key={feature}
                  >

                    <div className="feature-name">
                      {feature}
                    </div>


                    <div className="feature-bar">

                      <div
                        className="feature-bar-fill"
                        style={{
                          width: `${percentage}%`,
                        }}
                      />

                    </div>


                    <div className="feature-value">

                      {percentage.toFixed(2)}%

                    </div>

                  </div>

                );
              }
            )}

          </div>

        </section>

      </main>

    </div>
  );
}

export default Evaluation;