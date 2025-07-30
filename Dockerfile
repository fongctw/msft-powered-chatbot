FROM python:3.10-slim

WORKDIR /app

COPY . .

COPY .env .

RUN apt-get update && apt-get install -y git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir \
    flask \
    flask-cors \
    python-dotenv \
    azure-identity \
    msal \
    azure-ai-projects

EXPOSE 3000

CMD ["python", "main.py"]
