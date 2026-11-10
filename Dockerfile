# Imagen base oficial ligera de Python
FROM python:3.11-slim

# Evitar que Python genere archivos .pyc y activar unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema mínimas requeridas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Exponer puertos comunes (8501 local, 10000 Render)
EXPOSE 8501 10000

# Comando de inicio compatible con Render ($PORT dinámico asignado por la nube),
# modo headless y CORS/XSRF deshabilitado para permitir el WebSocket a través del proxy inverso de Render
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false"]
