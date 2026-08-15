FROM python:3.12-slim

# --------------------------------------------------
# Working directory
# --------------------------------------------------

WORKDIR /app


# --------------------------------------------------
# Python environment
# --------------------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# --------------------------------------------------
# Install system dependencies
# LibreOffice is required for DOCX -> PDF conversion
# --------------------------------------------------

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libreoffice \
        fonts-liberation \
    && rm -rf /var/lib/apt/lists/*


# --------------------------------------------------
# Install Python dependencies
# --------------------------------------------------

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY alembic ./alembic

# --------------------------------------------------
# Copy application
# --------------------------------------------------

COPY app ./app


# --------------------------------------------------
# Create resume export directory
# --------------------------------------------------

RUN mkdir -p /app/app/exports/resumes


# --------------------------------------------------
# Port
# --------------------------------------------------

EXPOSE 8000


# --------------------------------------------------
# Start FastAPI
# --------------------------------------------------

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]