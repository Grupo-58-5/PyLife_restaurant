from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



def get_app() -> FastAPI:
    app = FastAPI(
        title = "Restaurant and Reservation API by PyLife.dev",
        description="Project about a Restaurant and Reservation administration API by PyLife.dev",
        version = "0.1.0")
    

    CORSMiddleware(
        app=app,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=["*"],
        allow_headers=["*"]
    )

    # app.include_router(router=router, tags=["Calculadora"], prefix="/api/v1/calculadora")
    
    return app

app = get_app()

@app.get("/")
async def root():
    return {"message": "Aplicación funcionando"}
