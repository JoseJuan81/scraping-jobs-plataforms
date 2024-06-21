# Utiliza la imagen base de Debian 11 (Bullseye)
FROM debian:11

# Actualiza el sistema e instala las dependencias necesarias
RUN apt-get update && apt-get upgrade -y

# Instala Python 3.11 y otras dependencias
RUN apt-get install -y python3.10 python3-pip firefox-esr

# Instala las dependencias necesarias para Selenium
RUN apt-get install -y xvfb

WORKDIR /app

# Instala las bibliotecas Python requeridas
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Define el comando que se ejecutará al iniciar el contenedor
CMD ["python3", "main.py"]
