from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.shared.db.init_db import create_tables
from src.restaurants.infraestructure.routes.restaurant_routes import router as restaurant_router

async def lifespan(_: FastAPI):
    try:
        await create_tables()
        yield
    except RuntimeError as e:
        print(e)


def get_app() -> FastAPI:
    app = FastAPI(
        title = "Restaurant and Reservation API by PyLife.dev",
        description="Project about a Restaurant and Reservation administration API by PyLife.dev",
        version = "0.1.0",
        lifespan = lifespan
    )
    

    CORSMiddleware(
        app=app,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=["*"],
        allow_headers=["*"]
    )

    
    app.include_router(restaurant_router)
    return app

app = get_app()

@app.get("/")
async def root():
    return {"message": "Aplicación funcionando"}
