# Usa una imagen oficial ligera de Python
FROM python:3.11-slim

# Crea el directorio de trabajo
WORKDIR /app

# Copia e instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY . .

# Expone el puerto de la aplicación local
EXPOSE 8000

# Ejecuta el servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
