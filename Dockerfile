FROM python:3.13-slim
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y openssl
RUN API_KEY=$(openssl rand -hex 16) && echo "API_KEY=$API_KEY" >> /etc/environment

COPY app.py app.py
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 5000
CMD ["sh", "-c", "API_KEY=$(openssl rand -hex 16) && export API_KEY=$API_KEY && python3 -m flask run --host=0.0.0.0"]
