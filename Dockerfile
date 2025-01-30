FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /

ARG AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ARG AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

# Defina variáveis de ambiente
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

# Copy files
COPY property-friends-real-state-repo/property_friends_real_state/app/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port
EXPOSE 8000