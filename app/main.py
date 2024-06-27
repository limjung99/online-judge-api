from fastapi import FastAPI, Depends

from models.test_model import TestResponse, TestRequest
from dependencies.test_manager import TestManager, get_test_manager

app = FastAPI()


@app.get("/")
def get_index():
    return "hello,world!"


@app.post("/test/{test_id}", response_model=TestResponse)
def test_input(test_code: TestRequest, test_id: int, test_manager: TestManager = Depends(get_test_manager)):
    src = test_code.src

    with open(f"resources/code/{test_id}.py", "w") as f:
        f.write(src)

    test_response = test_manager.run_test(test_id)
    return test_response
