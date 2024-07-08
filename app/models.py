from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

user_organisation = Table(
    'user_organisation',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.userId')),
    Column('organisation_id', String, ForeignKey('organisations.orgId'))
)

class User(Base):
    __tablename__ = "users"
    userId = Column(String, primary_key=True, unique=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String)
    organisations = relationship("Organisation", secondary=user_organisation, back_populates="members")

class Organisation(Base):
    __tablename__ = "organisations"
    orgId = Column(String, primary_key=True, unique=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    members = relationship("User", secondary=user_organisation, back_populates="organisations")
