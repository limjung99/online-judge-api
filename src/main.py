from fastapi import FastAPI,Depends

from src.dependencies import get_test_manager
from src.test_manager import TestManager

app = FastAPI()

@app.get("/")
def get_index():
    return "hello,world!"

@app.post("/test/{test_id}")
def test_input(test_id:int,test_input:str,test_manager:TestManager = Depends(get_test_manager)):
    if test_manager.run_test()

