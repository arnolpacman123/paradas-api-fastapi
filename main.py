from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import lines_routes, lines_names

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lines_routes.router, prefix="/lines-routes", tags=["lines-routes"])
app.include_router(lines_names.router, prefix="/lines-names", tags=["lines-names"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
