import { useLocation, useNavigate } from "react-router-dom";
import "./PrescriptionPage.css";

function PrescriptionPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  if (!result) {
    return (
      <div className="prescription-container">
        <h2>No data available</h2>
        <button onClick={() => navigate("/")}>Go back</button>
      </div>
    );
  }

  const {
    date,
    age,
    gender,
    bmi,
    bmi_category,
    exercise_recommendations,
    model_diet_recommendation,
    disease_details,
  } = result;

  const detailed_diet_plan = disease_details.detailed_diet || {
    vegetarian: [],
    non_vegetarian: [],
    vegan: [],
  };

  const handleDownload = () => {
    fetch("http://localhost:5000/download-prescription", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ result }),
    })
      .then((res) => res.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `prescription_${date}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      })
      .catch((err) => console.error("Download failed", err));
  };

  return (
    <div className="prescription-container">
      <h1>MediMuse Prescription</h1>
      <p>
        <strong>Age:</strong> {age} | <strong>Gender:</strong> {gender}
      </p>
      <p>
        <strong>Date:</strong> {date}
      </p>

      <p>
        <strong>BMI:</strong> {bmi} ({bmi_category})
      </p>
      <p>
        <strong>AI Diet Plan:</strong> {model_diet_recommendation}
      </p>

      <div className="section">
        <h2>Disease</h2>
        <p>
          <strong>{disease_details.disease_name}</strong>
        </p>
        <p>{disease_details.description}</p>
      </div>

      <div className="section">
        <h3>Medications</h3>
        <ul>
          {disease_details.medication.map((med, i) => (
            <li key={i}>{med}</li>
          ))}
        </ul>
      </div>

      <div className="section">
        <h3>Precautions</h3>
        <ul>
          {disease_details.precautions.map((pre, i) => (
            <li key={i}>{pre}</li>
          ))}
        </ul>
      </div>

      <div className="section">
        <h3>Things to Do Now</h3>
        <ul>
          {disease_details.things_to_do_now.map((doNow, i) => (
            <li key={i}>{doNow}</li>
          ))}
        </ul>
      </div>

      <div className="section">
        <h3>Exercise Recommendations</h3>
        <ul>
          {exercise_recommendations.map((ex, i) => (
            <li key={i}>{ex}</li>
          ))}
        </ul>
      </div>

      <div className="section">
        <h3>Detailed Diet Plan</h3>

        <h4>Vegetarian</h4>
        <ul>
          {detailed_diet_plan.vegetarian.map((item, i) => (
            <li key={`veg-${i}`}>{item}</li>
          ))}
        </ul>

        <h4>Non-Vegetarian</h4>
        <ul>
          {detailed_diet_plan.non_vegetarian.map((item, i) => (
            <li key={`nonveg-${i}`}>{item}</li>
          ))}
        </ul>

        <h4>Vegan</h4>
        <ul>
          {detailed_diet_plan.vegan.map((item, i) => (
            <li key={`vegan-${i}`}>{item}</li>
          ))}
        </ul>
      </div>

      <button onClick={handleDownload}>📄 Download Prescription</button>
      <button onClick={() => navigate("/")}>🔙 New Prediction</button>
    </div>
  );
}

export default PrescriptionPage;
