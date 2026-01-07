# Plant Sentinel — Python FastAPI Project 

## What this project is
This is a Python-based conversion of your original Next.js frontend project into a backend-driven web application using **FastAPI**.
It includes:
- FastAPI backend with endpoints
- Simple HTML + Jinja2 template UI
- Image upload endpoint with a placeholder "plant health" prediction (color-based heuristic)
- Clear instructions to upgrade to a real ML model (PyTorch/TensorFlow)
- `requirements.txt`, Dockerfile, and deployment notes

## How to run (development)
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Open `http://localhost:8000/` in your browser.

## ML / AI upgrade notes
- The current `/api/predict` endpoint uses a lightweight heuristic (image color average) as a placeholder.
- To integrate a trained model:
  - Add your model file under `models/` and update `services/predict.py` to load and run the model.
  - Example options: PyTorch (`torch` + `torchvision`) or TensorFlow (`tensorflow`).
  - Ensure GPU support if needed and update Dockerfile accordingly.

## Files included
- `main.py` — FastAPI application with routes
- `services/predict.py` — prediction logic (placeholder + extension points)
- `templates/index.html` — simple UI for upload & viewing results
- `static/css/styles.css` — minimal styling
- `requirements.txt` — Python dependencies
- `Dockerfile` — optional containerization
- `README.md` — this file

## How to present this on your resume
- "Converted a React/Next.js frontend into a Python backend project using FastAPI. Implemented REST endpoints, image upload and a placeholder plant health predictor with clear upgrade path to integrate a trained ML model."

