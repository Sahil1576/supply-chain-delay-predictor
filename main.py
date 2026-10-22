from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from report_generator.pipeline_runner import PipelineRunner

from LLM.llm import llm

from report_generator.pipeline import Pipeline, model
from LLM.system_prompt import SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

structure_output = StrOutputParser()

@app.post("/predict")
def prediction(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file.")

    try:
        runner = PipelineRunner(
            llm=llm, 
            pipeline=Pipeline(csv_file=file.file, model=model),
            prompt=prompt,
            structure_output=structure_output
        )

        return runner.run()

    except KeyError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Missing required column in CSV: {e}. Expected 'Date' and 'Delayed' plus the model's features.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {e}")


# Must stay LAST so it does not shadow /predict.
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")