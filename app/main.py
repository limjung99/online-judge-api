from fastapi import FastAPI,Depends

from app.models.test_model import TestOutput
from app.dependencies.test_manager import TestManager,get_test_manager

app = FastAPI()

@app.get("/")
def get_index():
    return "hello,world!"

@app.post("/test/{test_id}")
def test_input(test_id:int,src:str,test_manager:TestManager = Depends(get_test_manager)):
    test_output = TestOutput()
    if test_manager.run_test(test_id,src):
        test_output.is_right = True
    else:
        test_output.is_right = False
    return test_output



