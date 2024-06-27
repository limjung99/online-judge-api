from app.dependencies.test_manager import TestManager, get_test_manager
from app.models.test_model import TestResponse, TestRequest
from fastapi import Depends, APIRouter

router = APIRouter()


@router.get("/")
def get_index():
    return "hello,world!"


@router.post("/test/{test_id}", response_model=TestResponse)
def test_input(test_code: TestRequest, test_id: int, test_manager: TestManager = Depends(get_test_manager)):
    src = test_code.src

    with open(f"app/resources/codes/{test_id}.py", "w") as f:
        f.write(src)

    test_response = test_manager.run_test(test_id)
    return test_response
