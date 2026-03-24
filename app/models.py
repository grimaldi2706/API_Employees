from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    cargo = Column(String)
    departamento = Column(String)
    salario = Column(Float)
    is_active = Column(Boolean, default=True)
