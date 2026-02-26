from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import users, children, milestones, reading_sessions, books
from app.api.dependencies import get_facade
from app.api import auth_dependencies
import firebase_admin
from firebase_admin import credentials
from .config import get_settings_class

from fastapi.middleware.cors import CORSMiddleware
from app.api.errors import register_error_handlers

import logging
logging.basicConfig(level=logging.DEBUG)


def create_app(settings=None) -> FastAPI:
    if settings is None:
        settings = get_settings_class()()
    
    if type(settings).__name__ == "ProductionConfig":
        cred = credentials.Certificate(settings.FIREBASE_CONFIG)
        firebase_admin.initialize_app(cred)

    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
    )

    app.state.settings = settings

    register_error_handlers(app)

    #Solving CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # router registrations
    app.include_router(users.router, prefix="/api", dependencies=[Depends(get_facade)])
    app.include_router(children.router, prefix="/api", dependencies=[Depends(get_facade)])
    app.include_router(milestones.router, prefix="/api", dependencies=[Depends(get_facade)])
    app.include_router(reading_sessions.router, prefix="/api", dependencies=[Depends(get_facade)])
    app.include_router(books.router, prefix="/api", dependencies=[Depends(get_facade)])
    app.include_router(auth_dependencies.router, prefix="/api")

    # root health check
    @app.get("/")
    def root():
        return {"status": "OK"}
    
    return app
