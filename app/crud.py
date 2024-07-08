from sqlalchemy.orm import Session
from app import models, schemas
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.userId == user_id).first()

def is_user_in_organisation(db: Session, user_id: int, target_user_id: int):
    # Logic to check if the user is in the same organization as the target user
    user_organisations = db.query(models.Organisation).filter(
        models.Organisation.members.any(userId=user_id)
    ).all()
    
    for organisation in user_organisations:
        if db.query(models.Organisation).filter(
            models.Organisation.orgId == organisation.orgId,
            models.Organisation.members.any(userId=target_user_id)
        ).first():
            return True
    
    return False

def user_has_access_to_organisation(db: Session, user_id: str, org_id: str) -> bool:
    # Check if there's a relationship between the user and the organisation
    access = db.query(models.Organisation).filter(
        models.Organisation.orgId == org_id,
        models.Organisation.members.any(userId=user_id)
    ).first()
    
    return access is not None

def get_organisation_by_id(db: Session, org_id: str):
    return db.query(models.Organisation).filter(models.Organisation.orgId == org_id).first()

def get_user_organisations(db: Session, user_id: str):
    user = get_user_by_id(db, user_id)
    return user.organisations if user else []

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        userId=str(uuid.uuid4()),
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        hashed_password=hashed_password,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_organisation(db: Session, org: schemas.OrganisationCreate, user: models.User):
    db_org = models.Organisation(
        orgId=str(uuid.uuid4()),
        name=org.name,
        description=org.description
    )
    db_org.members.append(user)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def add_user_to_organisation(db: Session, user: models.User, organisation: models.Organisation):
    organisation.members.append(user)
    db.commit()
