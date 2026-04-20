from fastapi import FastAPI

app = FastAPI()

@app.get("/detail")
def get_detail(): 
    return {
        "content": "Power Supply Unit",
        "status": "Available"
    }