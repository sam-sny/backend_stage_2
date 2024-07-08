from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app import models, database
from app.routers import auth, users, organisations

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "Bad request",
            "message": exc.detail,
            "statusCode": exc.status_code
        }
    )

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organisations.router)
