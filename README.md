# 🛡️ SafeSurf — Phishing Detection System

SafeSurf is a web-based phishing detection system that uses machine learning and URL analysis to identify malicious links and phishing emails in real-time.

---

## 🚀 Project Overview
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask/FastAPI)  
- **ML Models:** Random Forest, Naive Bayes  
- **Dataset:** Phishing Email and URL datasets (preprocessed for model training)  
- **Goal:** Protect users from phishing attacks through intelligent link and email analysis.

---

## ⚙️ Features
✅ Email phishing detection using ML  
✅ URL phishing classification  
✅ Integration with Google Safe Browsing API  
✅ Model-based prediction with pre-trained `.pkl` files  
✅ Interactive frontend interface for results visualization  

---

## 🧠 Machine Learning Details
- **Algorithms Used:** Random Forest, Naive Bayes  
- **Vectorization:** TF-IDF and Word2Vec  
- **Preprocessing:** Stopword removal, tokenization, stemming  
- **Training Data:** Cleaned phishing email datasets and URL datasets  

---

## 🖥️ Tech Stack
| Component | Technology |
|------------|-------------|
| Frontend | HTML, CSS, JS |
| Backend | Python (Flask / FastAPI) |
| ML | scikit-learn, XGBoost, Pandas |
| Deployment | (optional: add Flask/Gunicorn/Heroku if applicable) |

---

## 🧩 Folder Structure
safesurf/
├── backend/
│ ├── app.py
│ ├── emailcheckerml.py
│ ├── random_forest.py
│ ├── requirements.txt
│ └── ...
│
├── frontend/
│ ├── src/
│ ├── package.json
│ ├── style.css
│ └── ...
│
└── README.md

yaml
Copy code

---

## 🧠 How to Run Locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
