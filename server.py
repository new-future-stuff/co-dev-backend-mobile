from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel
from models import engine
import api


app = FastAPI()
app.include_router(api.router, prefix="/api")


@app.exception_handler(IntegrityError)
async def add_process_time_header(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"integrity_error": exc.orig.args[0]})
