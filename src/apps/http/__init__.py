from fastapi import FastAPI, Request, Query
from starlette.background import BackgroundTask

# Info, seems like this need to be at the top, also some have src before and others not (maybe due to relationship?)
from adapters.shared.beanie_models_adapter import UserDocument, EnergyDepositDocument, PlanetDocument
from apps.http.dependencies import get_middleware
from src.controllers.http import HttpController
import uvicorn
from decouple import config
from beanie import init_beanie
import motor.motor_asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import src.apps.http.dependencies as dependencies
import src.apps.http.settings
import logging as log
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
import asyncio
from src.core.buildable_items import BuildableItems, FinishBuildRequest
from src.core.planet_resources import PlanetResourcesUpdateRequest
from src.core.shared.models import AppBaseException
from src.apps.http.urls import register_fastapi_routes
import time
import logging



#@TODO: Add logger port
#@TODO: Websockets: https://github.com/tiangolo/fastapi/issues/685 --- https://fastapi.tiangolo.com/advanced/websockets/

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/metadata/
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SpaceRiders API",
        version="2.0.0",
        description="SpaceRiders API",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    openapi_schema['paths']['/jwt']['post']['description'] = "Get a JWT token to access protected resources"
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


async def exception_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        if isinstance(exc, AppBaseException):
            return JSONResponse(

                status_code=exc.code,
                content={"message": exc.msg},
            )

        log.critical("Something unexpected happened", exc)
        return JSONResponse(
            status_code=500,
            content={"message": "Error, something went wrong..."},
        )

# FastAPI hack to send back cors headers on exceptions. https://github.com/tiangolo/fastapi/issues/775
app.middleware('http')(exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def middleware(request: Request, call_next):
    items_use_case, planet_resources_use_case = await get_middleware()
    active_planet = request.headers.get("x-active-planet")
    if active_planet is not None:
        await items_use_case.finish_build(FinishBuildRequest(planet_id=active_planet))
        await planet_resources_use_case(PlanetResourcesUpdateRequest(planet_id=active_planet))

    return await call_next(request)


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(config("DB_URL"), )
    db = client[config('DB_NAME')]

    client.get_io_loop = asyncio.get_event_loop
    # await UserDocument.init_model(db, False)
    # await EnergyDepositDocument.init_model(db, False)
    # await PlanetDocument.init_model(db, False)
    # await TrollDocument.init_model(db, False)
    await init_beanie(database=db,
                      document_models=[UserDocument, EnergyDepositDocument, PlanetDocument]
                      )

@app.on_event("startup")
async def app_init():
    await dependencies.logging_adapter.info("Http App started")
    await init_db()



    http_controller = await dependencies.http_controller()
    urls = await register_fastapi_routes(http_controller)
    for url in urls:
        app.router.add_api_route(**url)


# if __name__ == "__main__":
#     uvicorn.run("__main__:app", port=8000, host='0.0.0.0', reload=True, workers=1, debug=True)