from sqlalchemy import Boolean, Column, Integer, LargeBinary, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, nullable=False, index=True)
    password = Column(LargeBinary, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)