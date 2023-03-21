from fastapi import Depends, HTTPException, Request
from db.session import get_db
from sqlalchemy.orm import Session
from db import models
from response_handler import error_response


async def validate_client_key(request: Request, db: Session=Depends(get_db)):
    # get the client key from the header.
    get_client_key = request.headers.get("Client-Authorization")
    # if the client key is missing throw an exception.
    if not get_client_key:
        return error_response.unauthorized_error(
            status_code=401, detail="Client key is missing")
    # check if the client key is valid.
    get_client = models.Client.check_single_key(db, get_client_key)
    if get_client is None:
        return error_response.unauthorized_error(
            status_code=401, detail="Client details not found")
    # client is inactive
    if get_client.status is False:
        return error_response.unauthorized_error(
            status_code=401, detail="Inactive account")
    # Store the data in the request state
    request.state.data = get_client
    
    return request
