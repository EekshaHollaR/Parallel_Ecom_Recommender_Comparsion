FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
# Create a dummy requirements.txt if it doesn't exist to prevent build failure in this context
# In a real scenario, requirements.txt should be populated.
# We'll assume the user will populate it or we can write a basic one.
RUN pip install --no-cache-dir flask flask-cors redis requests pandas numpy scipy rq

COPY . .

EXPOSE 5000

CMD ["python", "backend/api/app.py"]
