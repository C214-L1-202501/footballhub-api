from app.routes.routes_country import router as country
from app.routes.routes_championship import router as championship
import uvicorn

from fastapi import FastAPI

app = FastAPI()

app.include_router(country)
app.include_router(championship)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
