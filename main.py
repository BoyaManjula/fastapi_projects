from fastapi import FastAPI
from typing import Union

app = FastAPI()

# 1) root check
@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}

# 2) OPTION A: path parameter -> /hello/Manju
@app.get("/hello/{name}")
def hello_path(name: str):
    return {"message": f"Hello {name}!"}

# 3) OPTION B: query parameter -> /hello?name=Manju
@app.get("/hello")
def hello_query(name: Union[str, None] = None):
    if not name:
        name = "World"
    return {"message": f"Hello {name}!"}

