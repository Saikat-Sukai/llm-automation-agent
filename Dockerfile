FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app /app
RUN apt-get update && apt-get install -y nodejs npm
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]