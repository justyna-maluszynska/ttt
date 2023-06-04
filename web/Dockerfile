FROM python:3.10.11-alpine

# Ustaw katalog roboczy na /app
WORKDIR /app

# Skopiuj plik requirements.txt do kontenera
COPY requirements.txt .

# Zainstaluj zależności aplikacji
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę plików aplikacji do kontenera
COPY . /app

# Ustaw zmienne środowiskowe
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Uruchom aplikację przy starcie kontenera
CMD ["python", "-m", "flask", "run"]

