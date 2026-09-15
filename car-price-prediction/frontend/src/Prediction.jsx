import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Prediction() {

  const [options, setOptions] = useState({
    companies: [],
    fuel_types: [],
    models: [],
  });

  const [formData, setFormData] = useState({
    company: "",
    fuel_type: "",
    car_age: "",
    kms_driven: "",
    model_name: "",
  });

  const [prediction, setPrediction] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  // =========================================================
  // LOAD OPTIONS
  // =========================================================

  useEffect(() => {

    fetch("http://127.0.0.1:5000/options")

      .then((response) => {

        if (!response.ok) {
          throw new Error("Failed to load options");
        }

        return response.json();
      })

      .then((data) => {

        setOptions(data);

        setFormData((previous) => ({
          ...previous,

          company: data.companies?.[0] || "",

          fuel_type: data.fuel_types?.[0] || "",

          model_name: data.models?.[0] || "",
        }));

      })

      .catch((error) => {

        setError(error.message);

      });

  }, []);


  // =========================================================
  // HANDLE INPUT
  // =========================================================

  const handleChange = (event) => {

    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

  };


  // =========================================================
  // PREDICT PRICE
  // =========================================================

  const handleSubmit = async (event) => {

    event.preventDefault();

    setPrediction(null);

    setError("");

    setLoading(true);


    try {

      const response = await fetch(
        "http://127.0.0.1:5000/predict",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({

            company: formData.company,

            fuel_type: formData.fuel_type,

            car_age: Number(formData.car_age),

            kms_driven: Number(formData.kms_driven),

            model: formData.model_name,

          }),
        }
      );


      const data = await response.json();


      if (!response.ok || !data.success) {

        throw new Error(
          data.error || "Prediction failed"
        );

      }


      setPrediction(data.predicted_price);

    }

    catch (error) {

      setError(error.message);

    }

    finally {

      setLoading(false);

    }

  };


  // =========================================================
  // UI
  // =========================================================

  return (

    <div className="app">


      {/* NAVBAR */}

      <nav className="navbar">

        <div className="logo">
          Car Price Predictor
        </div>


        <div className="nav-links">

          <Link
            to="/"
            className="active"
          >
            Prediction
          </Link>


          <Link to="/evaluation">
            Evaluation
          </Link>

        </div>

      </nav>



      {/* MAIN */}

      <main className="main-container">


        <div className="page-header">

          <h1>
            Car Price Prediction
          </h1>

          <p>
            Enter the car details to estimate its resale price.
          </p>

        </div>



        {/* PREDICTION CARD */}

        <div className="prediction-card">

          <form onSubmit={handleSubmit}>


            <div className="form-grid">


              {/* COMPANY */}

              <div className="form-group">

                <label>
                  Company
                </label>


                <select
                  name="company"
                  value={formData.company}
                  onChange={handleChange}
                  required
                >

                  <option value="" disabled>
                    Select company
                  </option>


                  {options.companies.map(
                    (company) => (

                      <option
                        key={company}
                        value={company}
                      >
                        {company}
                      </option>

                    )
                  )}

                </select>

              </div>



              {/* FUEL TYPE */}

              <div className="form-group">

                <label>
                  Fuel Type
                </label>


                <select
                  name="fuel_type"
                  value={formData.fuel_type}
                  onChange={handleChange}
                  required
                >

                  <option value="" disabled>
                    Select fuel type
                  </option>


                  {options.fuel_types.map(
                    (fuel) => (

                      <option
                        key={fuel}
                        value={fuel}
                      >
                        {fuel}
                      </option>

                    )
                  )}

                </select>

              </div>



              {/* CAR AGE */}

              <div className="form-group">

                <label>
                  Car Age
                </label>


                <input
                  type="number"
                  name="car_age"
                  value={formData.car_age}
                  onChange={handleChange}
                  placeholder="Example: 5"
                  min="0"
                  required
                />

              </div>



              {/* KMS */}

              <div className="form-group">

                <label>
                  Kilometers Driven
                </label>


                <input
                  type="number"
                  name="kms_driven"
                  value={formData.kms_driven}
                  onChange={handleChange}
                  placeholder="Example: 45000"
                  min="0"
                  required
                />

              </div>

            </div>



            {/* MODEL */}

            <div className="form-group full-width">

              <label>
                Prediction Model
              </label>


              <select
                name="model_name"
                value={formData.model_name}
                onChange={handleChange}
                required
              >

                <option value="" disabled>
                  Select model
                </option>


                {options.models.map(
                  (model) => (

                    <option
                      key={model}
                      value={model}
                    >

                      {model
                        .replaceAll("_", " ")
                        .replace(/\b\w/g, (char) =>
                          char.toUpperCase()
                        )}

                    </option>

                  )
                )}

              </select>

            </div>



            {/* BUTTON */}

            <button
              type="submit"
              className="predict-button"
              disabled={loading}
            >

              {loading
                ? "Predicting..."
                : "Predict Price"}

            </button>

          </form>



          {/* ERROR */}

          {error && (

            <div className="error-message">
              {error}
            </div>

          )}



          {/* RESULT */}

          {prediction !== null && (

            <div className="result-box">

              <p>
                Estimated Price
              </p>


              <h2>

                ₹
                {Number(prediction).toLocaleString(
                  "en-IN",
                  {
                    maximumFractionDigits: 2,
                  }
                )}

              </h2>

            </div>

          )}

        </div>

      </main>

    </div>

  );
}

export default Prediction;