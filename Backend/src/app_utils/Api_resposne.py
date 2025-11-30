from fastapi.responses import JSONResponse


# -------------API------------------------------

class API_respone:
    def __init__(self ,statusCode , status_mesaage , data ):
        self.statusCode =statusCode
        self.status_message =status_mesaage
        self.data =data
    
    def api_respone(self):
        return JSONResponse(
            content={"message": self.status_message , "data" : self.data},
            status_code=self.statusCode
        )
    


#  ------------------Error Respone -----------------------------------------

class ErrorResponse:
    def __init__(self, statusCode: int, message: str):
        self.statusCode = statusCode
        self.message = message

    def send(self):
        return JSONResponse(
            content={"message": self.message},
            status_code=self.statusCode
        )


