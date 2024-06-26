from pydantic import BaseModel

class TestInput(BaseModel):
    src : str

class TestOutput(BaseModel):
    is_right : bool

