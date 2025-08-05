# Medimuse

Medimuse is a full-stack AI-powered healthcare web application designed to assist in real-time medical diagnosis and automated prescription generation. It uses NLP models to interpret user symptoms and generates downloadable PDF prescriptions.

---

## 🧠 Features

- Symptom-based medical diagnosis using NLP
- AI-powered prescription generation
- Downloadable PDF output
- Full-stack architecture with React frontend and Flask backend
- Clean UI with screenshots and supporting documents (`SS&pdf` folder)

---

## 🛠 Tech Stack

- **Frontend:** React.js, HTML, CSS, JavaScript
- **Backend:** Flask, Python
- **AI/NLP:** Sentence Transformers, Python NLP libraries
- **PDF Generation:** FPDF
- **Version Control:** Git, GitHub

---

## 📁 Folder Structure

Medimuse/
├── frontend/ # React frontend
├── backend/ # Flask backend with AI/NLP logic
├── SS&pdf/ # Screenshots and generated PDFs
└── README.md

---

## 🚀 Getting Started

1. **Clone the repo**

```bash
git clone https://github.com/bsomdatta/Medimuse.git
cd Medimuse

```

2.**Install frontend dependencies**

```bash
cd frontend
npm install
```

3.**Start frontend**

```bash
npm run dev

```

4.**Install backend dependencies**

```bash
cd ../backend
pip install -r requirements.txt
```

5.**Start backend**

```bash
python app.py
```
