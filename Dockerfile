FROM python:3.11-slim

#RUN apt-get -q -y update 
#RUN apt-get install -y gcc

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .

# TEST AUDIO FILE
COPY test.mp3 .

COPY alembic.ini .
COPY /alembic /alembic

COPY /app /app

COPY ./service_entrypoint.sh .

RUN chmod +x ./service_entrypoint.sh

ENV FLASK_APP=app

EXPOSE 5050
ENTRYPOINT [ "./service_entrypoint.sh" ]