from typing import Union
from app.routes.routes_country import router as country
import uvicorn

from fastapi import FastAPI

app = FastAPI()

app.include_router(country)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
