FROM python:3.11-slim

# Do not compile Bytecode
ENV PYTHONDONTWRITEBYTECODE=1
# Do not use output buffering
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /backend

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Run uvicorn in production mode (dev uses override in compose)
CMD ["uvicorn", "app.presentation.api.v1.main:app", "--host", "0.0.0.0", "--port", "8000"]
