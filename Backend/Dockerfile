FROM python:3.11-slim

WORKDIR /Backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirement.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
