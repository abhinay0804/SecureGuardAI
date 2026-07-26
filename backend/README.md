# 🚀 SecureGuard AI — Backend Service (FastAPI)

The backend service for **SecureGuard AI** is built using **FastAPI**, **Scikit-Learn ML models**, **NVIDIA NIM LLM Explainability**, and **MongoDB**.

---

## ⚙️ Architecture & Features

- **Fraud Prediction Router**: Combines machine learning inference with configurable velocity and anomaly business rules.
- **AI Explainability Engine**: Calls NVIDIA NIM (`meta/llama-3.1-70b-instruct`) or Google Gemini to generate natural language explanations for fraud analysts.
- **REST Endpoints**: Serves transaction analytics, KPI metrics, alerts, dynamic filtering, and user authentication.
- **Graceful Fallbacks**: Works out of the box with or without local MongoDB/Redis running.

---

## 🏃 Running the Backend

1. Navigate to `backend`:
   ```bash
   cd backend
   ```

2. Create virtual environment and install requirements:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the main server script:
   ```bash
   cd src/utils/fraud_dashboard
   python main.py
   ```

4. Server running on: **`http://localhost:8002`** (Swagger docs at **`http://localhost:8002/docs`**).
