from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI(title="API Employees", description="Prueba Técnica API con FastAPI")

@app.get("/")
def index():
    return {"message": "Bienvenido a la API Employees. Visita http://localhost:8000/docs para la documentación interactiva."}

@app.post("/api/employees", response_model=schemas.EmployeeResponse, status_code=201)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if db_emp:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    new_employee = models.Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@app.get("/api/employees", response_model=schemas.PaginatedEmployeeResponse)
def get_employees(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), db: Session = Depends(database.get_db)):
    offset = (page - 1) * limit
    
    # Solo listamos activos (Soft Delete logic)
    query = db.query(models.Employee).filter(models.Employee.is_active == True)
    total = query.count()
    employees = query.offset(offset).limit(limit).all()
    
    return {
        "data": employees,
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/employees/{id}", response_model=schemas.EmployeeResponse)
def get_employee(id: int, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == id, models.Employee.is_active == True).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return employee

@app.put("/api/employees/{id}", response_model=schemas.EmployeeResponse)
@app.patch("/api/employees/{id}", response_model=schemas.EmployeeResponse)
def update_employee(id: int, employee_update: schemas.EmployeeUpdate, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == id, models.Employee.is_active == True).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    update_data = employee_update.dict(exclude_unset=True)
    if "email" in update_data and update_data["email"] != employee.email:
        email_exists = db.query(models.Employee).filter(models.Employee.email == update_data["email"]).first()
        if email_exists:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
            
    for key, value in update_data.items():
        setattr(employee, key, value)
        
    db.commit()
    db.refresh(employee)
    return employee

@app.delete("/api/employees/{id}")
def delete_employee(id: int, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == id, models.Employee.is_active == True).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    # Soft delete: lo marcamos como inactivo en vez de borrar el registro
    employee.is_active = False
    db.commit()
    
    return {"message": "Empleado eliminado correctamente (Soft Delete)"}
