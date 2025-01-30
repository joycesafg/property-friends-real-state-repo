FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY ./property_friends_real_state/app/ /app/

# Install dependencies


# Expose port
EXPOSE 8000