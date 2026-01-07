from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
import io
from PIL import Image
import numpy as np

# Initialize FastAPI app
app = FastAPI(title="Plant Sentinel - AI Plant Health Diagnostics")

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Setup static files and templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def analyze_plant_image(image_bytes: bytes) -> dict:
    """
    Analyze plant health from image bytes.
    Uses color-based heuristic as placeholder for ML model.
    """
    try:
        # Open and process image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize for processing
        img = img.resize((224, 224))
        img_array = np.array(img)
        
        # Calculate color metrics
        avg_color = img_array.mean(axis=(0, 1))
        r, g, b = avg_color
        
        # Calculate health indicators
        green_ratio = g / (r + g + b + 1e-6)
        brown_ratio = (r + g) / (2 * (r + g + b) + 1e-6)
        brightness = (r + g + b) / 3
        
        # Determine health status
        if green_ratio > 0.4 and brightness > 80:
            label = "Healthy Plant"
            confidence = min(95.0, green_ratio * 200)
            recommendation = "🌿 Your plant looks healthy! Continue regular watering and ensure adequate sunlight. Monitor for any changes in leaf color or texture."
            status = "healthy"
            color = "#10b981"
            
        elif brown_ratio > 0.45 or brightness < 60:
            label = "Nutrient Deficiency"
            confidence = min(88.0, brown_ratio * 180)
            recommendation = "💊 Your plant may have a nutrient deficiency. Consider using a balanced fertilizer (N-P-K 10-10-10). Ensure proper pH levels and check drainage."
            status = "warning"
            color = "#f59e0b"
            
        elif r > g * 1.2:
            label = "Disease or Stress Detected"
            confidence = min(82.0, (r / (g + 1e-6)) * 40)
            recommendation = "⚠️ Your plant shows signs of stress or disease. Check for pests, ensure proper watering, and improve air circulation. Consider isolating from other plants."
            status = "unhealthy"
            color = "#ef4444"
            
        else:
            label = "Needs Attention"
            confidence = 75.0
            recommendation = "🔍 Your plant needs attention. Check soil moisture, light conditions, and look for signs of pests or diseases. Adjust care routine as needed."
            status = "caution"
            color = "#3b82f6"
        
        return {
            "success": True,
            "label": label,
            "confidence": round(confidence, 1),
            "recommendation": recommendation,
            "status": status,
            "color": color,
            "metrics": {
                "green_ratio": round(green_ratio, 3),
                "brown_ratio": round(brown_ratio, 3),
                "brightness": round(brightness, 1)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "label": "Error Processing Image",
            "confidence": 0.0,
            "recommendation": f"Unable to analyze image: {str(e)}",
            "status": "error",
            "color": "#ef4444"
        }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": None
    })


@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    """
    API endpoint for plant health prediction
    Returns JSON response
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid file type. Please upload an image."}
            )
        
        # Read image bytes
        contents = await file.read()
        
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Analyze image
        result = analyze_plant_image(contents)
        result["filename"] = file.filename
        
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Server error: {str(e)}"}
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Plant Sentinel API"}


if __name__ == "__main__":
    print("🌿 Starting Plant Sentinel...")
    print("📍 Server running at: http://localhost:8000")
    print("🔄 Auto-reload enabled for development")
    print("\n✨ Press CTRL+C to stop the server\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
