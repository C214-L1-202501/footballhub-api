from app.routes.routes_country import router as country
from app.routes.routes_championship import router as championship
from app.routes.routes_stadium import router as stadium
from app.routes.routes_player import router as player
from app.routes.routes_team import router as team
import uvicorn

from fastapi import FastAPI

app = FastAPI()

app.include_router(country)
app.include_router(championship)
app.include_router(stadium)
app.include_router(player)
app.include_router(team)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
