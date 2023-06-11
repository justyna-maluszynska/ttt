FROM python:3.10.11-alpine

# Ustaw katalog roboczy na /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_RUN_HOST=0.0.0.0

# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["sh", "entrypoint.sh"]


