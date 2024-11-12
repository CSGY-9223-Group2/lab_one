FROM python:3.12-slim
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
WORKDIR /app

RUN pip install pipenv

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y openssl
RUN API_KEY=$(openssl rand -hex 16) && echo "API_KEY=$API_KEY" >> /etc/environment

COPY app.py app.py
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile --python $(which python3)

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 5000
CMD ["sh", "-c", "API_KEY=$(openssl rand -hex 16) && export API_KEY=$API_KEY && pipenv run python3 -m flask run --host=0.0.0.0"]
