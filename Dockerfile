FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY property_friends_real_state/app/ /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
