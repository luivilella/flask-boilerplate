FROM python:3.7

EXPOSE 5000

ADD ./application/requirements.txt /deploy/requirements.txt

WORKDIR /deploy

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python manage.py runserver
