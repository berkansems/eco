FROM python:3.6.8-jessie

COPY requirements.txt /
RUN pip install -r requirements.txt

RUN mkdir ecommerce
RUN mkdir /var/log/docklog


COPY . ./ecommerce
WORKDIR /ecommerce

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000/tcp
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]