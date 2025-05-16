FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt 

EXPOSE 80

CMD [ "python", "manage.py", "runserver", "0.0.0.0:80"]