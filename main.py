# main.py
from fastapi import FastAPI
from bootstrap import start_system
app = FastAPI()

start_system()
@app.get("/")
def read_root():
    return {"Hello": "World"}
