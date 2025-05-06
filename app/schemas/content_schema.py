from pydantic import BaseModel


class InputProcess(BaseModel):
    input: str

# class InputResponse(BaseModel):
#     positioning: str
#     persona: str
#     target: str  

class ContentResponse(BaseModel):
    response: str