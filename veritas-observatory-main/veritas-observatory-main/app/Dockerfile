FROM python:3.8


COPY ./requirements.txt /app/requirements.txt
COPY . /app

WORKDIR /app
RUN pip3 install -r requirements.txt

ENV FLASK_ENV=production
ENV FLASK_APP=app.py
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
