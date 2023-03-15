from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class Exceptions:
    def __init__(self):
        pass
    
    def client_exists_error(self):
        return JSONResponse(
            status_code= 409,
            content=jsonable_encoder({"detail": "Client already exists"}),
        )
         
    def service_error(self, status_code, detail):
        return JSONResponse(
            status_code= status_code,
            content=jsonable_encoder({"detail": detail}),
        )
        
exceptions = Exceptions()
    