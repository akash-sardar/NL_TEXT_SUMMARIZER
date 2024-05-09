from fastapi import FastAPI
import uvicorn
import sys
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from NLPTextSummarizer.pipeline.prediction import PredcitionPipeline


text:str = "What is Text Summarization ?"
app = FastAPI()

# default route
@app.get("/", tags = ["authentication"])
async def index():
    return RedirectResponse(url = "/docs")


# route for training
@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training Successful")
    except Exception as e:
        return Response(f" Error occured: {e}")



# route for prediction
@app.post("/predict")
async def predict_route(text):
    try:
        obj = PredcitionPipeline()
        text = obj.predict(text)
        return text
    except Exception as e:
        raise e
    


# To run initialize host and port
if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8080)