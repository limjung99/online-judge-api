from fastapi import FastAPI, Depends
from app.api import test_api

app = FastAPI()
app.include_router(test_api.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)
