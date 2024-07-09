from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app import schemas, crud, models, database, auth
from fastapi.responses import JSONResponse
from jose import JWTError, jwt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.RegisterResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = crud.create_user(db, user)
    org_name = f"{new_user.firstName}'s Organisation"
    org_description = "Default description"  # Provide a default value or fetch it from user input
    organisation_data = {"name": org_name, "description": org_description}
    crud.create_organisation(db, schemas.OrganisationCreate(**organisation_data), new_user)

    access_token = auth.create_access_token(data={"sub": new_user.email})

    # Prepare the response data in the required format
    response_data = {
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": access_token,
            "user": {
                "userId": str(new_user.userId),  # Ensure userId is converted to string if necessary
                "firstName": new_user.firstName,
                "lastName": new_user.lastName,
                "email": new_user.email,
                "phone": new_user.phone
            }
        }
    }

    return response_data  # Return the prepared response data


@router.post("/login", responses={200: {"model": schemas.LoginResponse}, 401: {"model": schemas.ErrorResponse}})
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        return JSONResponse(
            status_code=401,
            content={
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401
            }
        )

    access_token = auth.create_access_token(data={"email": user.email})

    response_data = {
        "status": "success",
        "message": "Login successful",
        "data": {
            "accessToken": access_token,
            "user": {
                "userId": str(user.userId),  # Ensure userId is converted to string if necessary
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email,
                "phone": user.phone
            }
        }
    }

    return response_data
