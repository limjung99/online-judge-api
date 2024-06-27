from typing import Optional

from pydantic import BaseModel

class TestRequest(BaseModel):
    src: str

class TestResponse(BaseModel):
    test_id: int
    is_right: bool
    result: Optional[str] = None
    err: Optional[str] = None

