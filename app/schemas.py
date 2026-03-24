from pydantic import BaseModel, EmailStr
from typing import Optional

class EmployeeBase(BaseModel):
    nombre: str
    email: EmailStr
    cargo: str
    departamento: str
    salario: float

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    cargo: Optional[str] = None
    departamento: Optional[str] = None
    salario: Optional[float] = None

class EmployeeResponse(EmployeeBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class PaginatedEmployeeResponse(BaseModel):
    data: list[EmployeeResponse]
    total: int
    page: int
    limit: int
