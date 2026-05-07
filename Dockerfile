FROM python:3.13-slim

WORKDIR /app

# PDF aur OCR ke liye system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD uvicorn src.api.main:app --host 0.0.0.0 --port 7860