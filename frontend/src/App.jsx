// import { useState } from "react";
// import "./App.css";
// import PrescriptionCard from "./assets/prescription.jsx";

// function App() {
//   const [mode, setMode] = useState("text");
//   const [symptoms, setSymptoms] = useState("");
//   const [age, setAge] = useState("");
//   const [weight, setWeight] = useState("");
//   const [gender, setGender] = useState("Male");
//   const [image, setImage] = useState(null);
//   const [result, setResult] = useState(null); // ✅ Store the full prediction object
//   const [darkMode, setDarkMode] = useState(false); // 🔥 Dark mode toggle

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (mode === "text") {
//       const response = await fetch("http://localhost:5000/predict-text", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ symptoms, age, weight, gender }),
//       });
//       const data = await response.json();
//       setResult(data); // ✅ Set full data object
//     } else {
//       const formData = new FormData();
//       formData.append("image", image);
//       const response = await fetch("http://localhost:5000/predict-image", {
//         method: "POST",
//         body: formData,
//       });
//       const data = await response.json();
//       setResult(data); // ✅ In case you extend it to image-based prediction
//     }
//   };

//   return (
//     <div className={`fullscreen-container ${darkMode ? "dark" : ""}`}>
//       <div className="form-card">
//         <div className="logo-title">
//           <h1 className="app-title">MediMuse</h1>
//           <p className="tagline">Predict. Prevent. Prosper.</p>
//         </div>

//         <button className="toggle-btn" onClick={() => setDarkMode(!darkMode)}>
//           {darkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
//         </button>

//         <div className="tab-switch">
//           <button
//             className={mode === "text" ? "active" : ""}
//             onClick={() => setMode("text")}
//           >
//             Text-based
//           </button>
//           <button
//             className={mode === "image" ? "active" : ""}
//             onClick={() => setMode("image")}
//           >
//             Image-based
//           </button>
//         </div>

//         <form onSubmit={handleSubmit}>
//           {mode === "text" && (
//             <>
//               <input
//                 type="text"
//                 placeholder="Enter symptoms"
//                 value={symptoms}
//                 onChange={(e) => setSymptoms(e.target.value)}
//                 required
//               />
//               <input
//                 type="number"
//                 placeholder="Age"
//                 value={age}
//                 onChange={(e) => setAge(e.target.value)}
//                 required
//               />
//               <input
//                 type="number"
//                 placeholder="Weight (kg)"
//                 value={weight}
//                 onChange={(e) => setWeight(e.target.value)}
//                 required
//               />
//               <select
//                 value={gender}
//                 onChange={(e) => setGender(e.target.value)}
//               >
//                 <option>Male</option>
//                 <option>Female</option>
//                 <option>Other</option>
//               </select>
//             </>
//           )}

//           {mode === "image" && (
//             <input
//               type="file"
//               accept="image/*"
//               onChange={(e) => setImage(e.target.files[0])}
//               required
//             />
//           )}

//           <button type="submit">Predict</button>
//         </form>

//         {result && (
//           <div style={{ marginTop: "2rem" }}>
//             <PrescriptionCard data={result} />
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// export default App;

import { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useNavigate,
} from "react-router-dom";
import "./App.css";
import PrescriptionPage from "./assets/prescription.jsx";

function FormPage() {
  const [mode, setMode] = useState("text");
  const [symptoms, setSymptoms] = useState("");
  const [age, setAge] = useState("");
  const [weight, setWeight] = useState("");
  const [height, setHeight] = useState("");
  const [gender, setGender] = useState("Male");
  const [image, setImage] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const [loading, setLoading] = useState(false); // 🆕 loading state

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // 🆕 show spinner

    try {
      let data;
      if (mode === "text") {
        const response = await fetch("http://localhost:5000/predict-text", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            // patient_name: patientName,
            symptoms,
            age,
            weight,
            height,
            gender,
          }),
        });
        data = await response.json();
      } else {
        const formData = new FormData();
        formData.append("image", image);
        const response = await fetch("http://localhost:5000/predict-image", {
          method: "POST",
          body: formData,
        });
        data = await response.json();
      }

      navigate("/prescription", { state: { result: data } });
    } catch (err) {
      alert("An error occurred. Please try again.");
      console.error(err);
    } finally {
      setLoading(false); // 🆕 hide spinner
    }
  };

  return (
    <div className={`fullscreen-container ${darkMode ? "dark" : ""}`}>
      <div className="form-card">
        <div className="logo-title">
          <h1 className="app-title">MediMuse</h1>
          <p className="tagline">Predict. Prevent. Prosper.</p>
        </div>

        <button className="toggle-btn" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
        </button>

        <div className="tab-switch">
          <button
            className={mode === "text" ? "active" : ""}
            onClick={() => setMode("text")}
          >
            Text-based Disease Prediction
          </button>
        </div>

        {loading ? (
          <div className="spinner-container">
            <div className="spinner"></div>
            <div>Generating prescription, please wait...</div>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            {mode === "text" && (
              <>
                {/* <input
                  type="text"
                  placeholder="Patient Name"
                  value={patientName}
                  onChange={(e) => setPatientName(e.target.value)}
                  required
                /> */}
                <input
                  type="text"
                  placeholder="Enter symptoms"
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  required
                />
                <input
                  type="number"
                  placeholder="Age"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  required
                />
                <input
                  type="number"
                  placeholder="Weight (kg)"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  required
                />
                <input
                  type="number"
                  placeholder="Height (m)"
                  value={height}
                  onChange={(e) => setHeight(e.target.value)}
                  required
                />
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                >
                  <option>Male</option>
                  <option>Female</option>
                  <option>Other</option>
                </select>
              </>
            )}
            {mode === "image" && (
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setImage(e.target.files[0])}
                required
              />
            )}
            <button type="submit" disabled={loading}>
              {loading ? "Predicting..." : "Predict"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FormPage />} />
        <Route path="/prescription" element={<PrescriptionPage />} />
      </Routes>
    </Router>
  );
}

export default App;
