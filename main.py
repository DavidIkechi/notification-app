# The main point of call.
from fastapi import FastAPI, Depends
from schema import *
from db.session import Base, Session, engine
from db import models
from jobs.job_config import notification_schedule
from apis.client import client_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, asyncio
import os, uuid

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
    await asyncio.wait([scheduler, api])

# include router.
notification_app.include_router(
    client_router
)
@notification_app.get("/")
async def ping():
    return {"detail": "Notification Application is up"}

if __name__ == "__main__":
    # Run both applications
    asyncio.run(main())