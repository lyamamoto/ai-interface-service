FROM python:3.11-slim

#RUN apt-get -q -y update 
#RUN apt-get install -y gcc

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .

COPY alembic.ini .
COPY /alembic /alembic

COPY /app /app

COPY ./service_entrypoint.sh .

ENV FLASK_APP=app

EXPOSE 5000
ENTRYPOINT [ "./service_entrypoint.sh" ]