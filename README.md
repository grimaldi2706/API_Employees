# API de Gestión de Empleados

Esta API RESTful proporciona un sistema para la gestión de registros de empleados, construida utilizando **Python**, **FastAPI** y el ORM **SQLAlchemy**. Está diseñada para integrarse de forma fluida con bases de datos relacionales como **MySQL** y se encuentra orquestada mediante **Docker** para asegurar la reproducibilidad del entorno.

## Características Técnicas

*   **Arquitectura RESTful**: Provisión de endpoints estandarizados para operaciones CRUD de la entidad Empleado.
*   **Paginación Eficiente**: Implementada de manera nativa en el listado base (`GET /api/employees`) para asegurar el alto rendimiento e indexado frente a grandes volúmenes de registros.
*   **Gestión de Eliminaciones Lógicas (Soft Delete)**: Preservación garantizada de la integridad referencial y el historial de transacciones, actualizando un indicador interno de estado (`is_active = False`) en lugar de borrar la información real.
*   **Validación Estricta de Datos**: Esquematización formal regida por *Pydantic*, confirmando que los flujos de entrada y salida respeten en todo segundo momento las especificaciones técnicas trazadas y los tipos de datos.
*   **Orquestación Basada en Contenedores**: Infraestructura predefinida vía `Dockerfile` y `docker-compose.yml`, lista para montarse y empaquetarse minimizando configuraciones de runtime.

## Requisitos de Entorno

*   Plataforma de virtualización [Docker](https://docs.docker.com/get-docker/) y orquestador [Docker Compose](https://docs.docker.com/compose/install/) instalados y configurados.
*   Un clúster, instancia remota o servicio local operativo de la base de datos **MySQL** accesible por red o bridge.

## Guía Técnica de Despliegue

### 1. Inicialización de la Base de Datos
El repositorio provee el script estructural `database.sql` con el DDL (Data Definition Language) de la aplicación.
Ejecute este archivo contra el servidor objetivo para aprovisionar orgánicamente la base de datos transaccional requerida y sus respectivas tablas:
```bash
mysql -u root -p < database.sql
```

### 2. Configuración de Variables Analíticas
Asegúrese de inyectar las credenciales relacionales pertinentes modificando las variables asignadas al servicio en el archivo `docker-compose.yml`:
```yaml
environment:
  - MYSQL_USER=su_usuario
  - MYSQL_PASSWORD=su_contraseña
  - MYSQL_HOST=host.docker.internal # Refiera la IP correspondiente en caso de ser un host remoto.
  - MYSQL_PORT=3306
  - MYSQL_DB=employees_db
```
*(Nota Técnica: Aprovechar apuntar al dominio DNS interno `host.docker.internal` permite solventar la interconexión con el entorno local del sistema host al operar en Docker Desktop).*

### 3. Compilación y Puesta en Servicio
Posiciónese en directorio primario (raíz) a través de la interfaz terminal o powershell local y ordene el comando base de montaje:
```bash
docker-compose up --build -d
```
Verifique la correcta estabilización del runtime constatando con éxito la exposición del servicio sobre el puerto reservado `8000`.

## Documentación Funcional de Endpoints

Una vez el contenedor se notifique operativo, diríjase a la interfaz OpenAPI incrustada para consultar métricas, requerimientos JSON e interactuar lógicamente en:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

### Endpoints 

| Método   | Endpoint                  | Comportamiento del Recurso                                 |
| -------- | ------------------------- | ---------------------------------------------------------- |
| **POST** | `/api/employees`          | Adición e inserción de una nueva entidad referencial.       |
| **GET**  | `/api/employees`          | Retorna catálogo activo mediante paginaciones calculadas.  |
| **GET**  | `/api/employees/{id}`     | Inspección de propiedades primarias a través de su PK ID.   |
| **PUT/PATCH**| `/api/employees/{id}` | Mutación y refinamiento de la data de objeto específico.    |
| **DELETE**   | `/api/employees/{id}` | Acción para de-activación sistemática (*Soft Delete*).      |
