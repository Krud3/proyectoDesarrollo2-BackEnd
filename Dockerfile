# Usa una imagen base de Python
FROM python:3.9-alpine3.17

# Configura variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo en /code
WORKDIR /code

# Copia los directorios auction_app y drf a tu contenedor
COPY auction_app /code/auction_app/
COPY drf /code/drf/

# Copia el archivo manage.py a tu contenedor
COPY manage.py /code/

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt /code/

# Instala las dependencias del proyecto especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Crear un usuario no privilegiado
RUN adduser -D myuser

# Cambiar al usuario no privilegiado
USER myuser

# Expone el puerto 8000 para que pueda ser accesible desde fuera del contenedor
EXPOSE 8000

# Define el comando para arrancar la aplicac
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
