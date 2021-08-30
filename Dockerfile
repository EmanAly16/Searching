FROM python:3.8.10
ADD . /code
WORKDIR /code

#ENV FLASK_APP=app.py

RUN pip install -r requirements.txt

#CMD ["flask", "run"]
