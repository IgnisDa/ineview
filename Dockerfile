FROM python:3.10-buster
RUN apt update && \
    apt install -y ffmpeg libgl1 && \
    pip3 install poetry
WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --dev && \
    pip install -r requirements.txt
COPY . .
ARG DATABASE_URL \
    DJANGO_SECRET_KEY
ENV DATABASE_URL="${DATABASE_URL}" \
    DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY}" \
    DJANGO_DEBUG="False" \
    CI="1"
EXPOSE 80
CMD cd apps/server && \
    python manage.py collectstatic --noinput && \
    python manage.py migrate --noinput && \
    gunicorn -b 0.0.0.0:80 server.wsgi:application --access-logfile - --error-logfile -
