# The main point of call.
from fastapi import FastAPI, Depends
from schema import *
from db.session import Base, engine, Session
from sqlalchemy.orm import Session as session_local
from db import models
from db.session import get_db
from jobs.job_config import notification_schedule
from apis.client import client_router
from apis.notification import notification_router
from apis.transport_type import trans_config_router
from apis.noti_variables import noti_variable_router
from apis.trans_method import trans_type_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, asyncio
import os, uuid, multiprocessing
from tests.seeder import (
    seed_transport_channel,
    seed_notification_type,
    seed_channel_transport,
    seed_transport_configuration,
    seed_active_channel_client_config,
    seed_notification_variable
)

# Microservice description
description = "Notification Application"
tags_metadata =[
    {
        "name":"Client",
        "description":"Client Notification Crud",
    }
]

notification_app = FastAPI(
    title="Notification API",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# create the tables.
models.Base.metadata.create_all(engine)

# allowed host.
origins =[]
notification_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)

# configure both API and Rocketry to run Asyschronously.
class Server(uvicorn.Server):
    """Customized uvicorn.Server
    
    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""
    def handle_exit(self, sig: int, frame) -> None:
        notification_schedule.session.shut_down()
        return super().handle_exit(sig, frame)

async def main() -> None:
    server = Server(uvicorn.Config(
        "main:notification_app", 
        host=os.getenv("HOST"), 
        port=int(os.getenv("NOTI_PORT")), 
        reload=os.getenv("RELOAD"),
        workers=1, 
        loop="asyncio")
    )
    
    api = asyncio.create_task(server.serve())
    scheduler = asyncio.create_task(notification_schedule.serve())

    # Wait for all tasks to complete
    await asyncio.wait([scheduler, api])

# include client router.
notification_app.include_router(
    client_router
)

# include notification router.
notification_app.include_router(
    notification_router
)

# include the transport config router.
notification_app.include_router(
    trans_config_router
)

# include the transport method router.
notification_app.include_router(
    trans_type_router
)

# include the notification variable router.
notification_app.include_router(
    noti_variable_router
)

@notification_app.on_event("startup")
async def startup_event():
    db = Session()
    seed_transport_channel(db)
    seed_notification_type(db)
    seed_channel_transport(db)
    seed_notification_variable(db)
    db.close()
    
    
@notification_app.get("/")

async def ping():
    return {"detail": "Notification Application is up"}

if __name__ == "__main__":
    # Run the FastAPI app
    asyncio.run(main())
