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

@app.get("/", response_class=JSONResponse)
def read_root():
    return {
        "statusCode": 200,
        "message": "Welcome to the User Authentication and Organisation API",
        "endpoints": {
            "/auth/register": "POST - Register a new user",
            "/auth/login": "POST - Log in a user",
            "/api/users/:id": "GET - Get user details [PROTECTED]",
            "/api/organisations": "POST - Create a new organisation [PROTECTED]",
            "/api/organisations/:orgId": "GET - Get a single organisation record [PROTECTED]",
            "/api/organisations/:orgId/users": "POST - Add a user to an organisation [PROTECTED]"
        }
    }

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organisations.router)
