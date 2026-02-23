FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pydantic-settings

# Copy project
COPY . .

# Create logs directory
RUN mkdir -p logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]