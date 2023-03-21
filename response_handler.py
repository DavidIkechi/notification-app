from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

# for errorsS
class Exceptions:
    def __init__(self):
        pass
    
    def bad_request_error(self, status=0, status_code=400, detail="An error occurred"):
        return JSONResponse(
            status_code= status_code,
            content=jsonable_encoder({"detail": detail,
                                      "status": status}),
        )    
    
    def unauthorized_error(self, status_code = 401, detail="Client is Unanthorized"):
        raise HTTPException(status_code = status_code, detail=detail)
         
    def server_error(self, status_code=500, status = 0, detail = ""):
        raise HTTPException(status_code = status_code, detail=detail)

# for success message.       
class Success:
    def __init__(self):
        pass
    
    def success_message(self, status_code=200, status=1, detail=None):
        return JSONResponse(
            status_code= status_code,
            content=jsonable_encoder({"detail": detail,
                                      "status": status}),
        )
    
    
error_response = Exceptions()
success_response = Success()