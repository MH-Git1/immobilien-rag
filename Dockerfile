FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py api.py ./
COPY frontend/ frontend/
COPY data_pdf/ data_pdf/

ENV NLTK_DISABLE_IMPORT_SECURITY=1

# $PORT wird von Render zur Laufzeit vorgegeben; 8000 als lokaler Fallback
# (z.B. für `docker run -p 8000:8000 ...` ohne Render).
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]
