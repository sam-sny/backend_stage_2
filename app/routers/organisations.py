from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app import schemas, crud, database, auth
from uuid import uuid4

router = APIRouter(prefix="/api/organisations", tags=["organisations"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
organizations = []

@router.get("/", response_model=dict)
def read_user_organisations(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = auth.decode_access_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user_by_email(db, email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    organisations = crud.get_user_organisations(db, user_id=user.userId)
    
    return {
        "status": "success",
        "message": "Organisations retrieved successfully",
        "data": {
            "organisations": [
                {
                    "orgId": org.orgId,
                    "name": org.name,
                    "description": org.description,
                } for org in organisations
            ]
        }
    }

@router.get("/{orgId}", response_model=schemas.OrganisationResponse)
def read_organisation(orgId: str, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = auth.decode_access_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = crud.get_user_by_email(db, email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    organisation = crud.get_organisation_by_id(db, org_id=orgId)
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")
    if not crud.user_has_access_to_organisation(db, user_id=user.userId, org_id=orgId):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return {
        "status": "success",
        "message": "Organisation retrieved successfully",
        "data": {
            "orgId": organisation.orgId,
            "name": organisation.name,
            "description": organisation.description,
        }
    }

@router.post("/", response_model=schemas.OrganisationResponse, status_code=status.HTTP_201_CREATED)
def create_organisation(organisation: schemas.OrganisationCreateRequest):
    # Generate unique orgId (for demonstration, use uuid4, replace with actual logic)
    org_id = str(uuid4())

    # Create organisation object
    new_organisation = {
        "orgId": org_id,
        "name": organisation.name,
        "description": organisation.description,
    }

    # Add to in-memory storage
    organizations.append(new_organisation)

    # Return success response
    return {
        "status": "success",
        "message": "Organisation created successfully",
        "data": new_organisation,
    }

@router.post("/{orgId}/users", response_model=dict)
def add_user_to_organisation(orgId: str, user_data: schemas.AddUserRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = auth.decode_access_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user_by_email(db, email=token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    organisation = crud.get_organisation_by_id(db, org_id=orgId)
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")
    user_to_add = crud.get_user_by_id(db, user_id=user_data.userId)
    if not user_to_add:
        raise HTTPException(status_code=404, detail="User to add not found")
    crud.add_user_to_organisation(db, user_to_add, organisation)
    return {
        "status": "success",
        "message": "User added to organisation successfully",
    }
