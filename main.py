from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from report_generator.report_generator import main

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Supply Chain Delay Predictor")

# Only needed if the UI is opened from a different origin (e.g. Live Server on :5500).
# Not needed when the UI is served by FastAPI itself (see the mount below).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your real domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
def prediction(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file.")

    try:
        return main(file.file)
    except KeyError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Missing required column in CSV: {e}. Expected 'Date' and 'Delayed' plus the model's features.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {e}")


# Must stay LAST so it does not shadow /predict.
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")