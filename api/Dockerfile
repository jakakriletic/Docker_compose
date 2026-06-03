FROM python:3.11-slim
WORKDIR /endpoints
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["fastapi", "run", "endpoint.py", "--port", "80"]