from fastapi import FastAPI,Depends

from app.models.test_model import TestOutput
from app.dependencies.test_manager import TestManager,get_test_manager

app = FastAPI()

@app.get("/")
def get_index():
    return "hello,world!"

@app.post("/test/{test_id}")
def test_input(test_id:int,src:str,test_manager:TestManager = Depends(get_test_manager)):
    # TODO
    # later change it test problem case by case ;;
    with open("app/resources/inputs/input1.txt") as f:
        test_input = f.read()

    with open("app/resources/outputs/output1.txt") as f:
        test_output = f.read()

    if test_manager.run_test(src,test_input,test_output):
        return True
    else:
        return False



