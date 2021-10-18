FROM python:3.8.5

WORKDIR /code
COPY foodgram /code
RUN pip install --upgrade pip &&\
    pip install -r /code/requirements.txt &&\
    python managy.py makemigrations &&\
    python managy.py migrate &&\
    python managy.py collectstatic
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
