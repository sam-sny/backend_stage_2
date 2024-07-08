from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, database, auth, models
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_record(id: str, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_id(db, user_id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the current user is allowed to view this record
    if user.userId != current_user.userId and not crud.is_user_in_organisation(db, user_id=current_user.userId, target_user_id=id):
        raise HTTPException(status_code=403, detail="Not authorized to access this user")

    response_data = {
        "status": "success",
        "message": "User record retrieved successfully",
        "data": {
            "userId": str(user.userId),
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "phone": user.phone
        }
    }

    return response_data
