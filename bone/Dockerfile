FROM alpine:3.4

ENV PYTHONUNBUFFERED 1

ENV APP_PATH /bone

RUN apk --update add uwsgi python3 python3-dev build-base linux-headers postgresql-dev jpeg-dev zlib-dev
RUN pip3 install --upgrade pip

COPY requirements.txt $APP_PATH/requirements.txt
RUN pip3 install -r $APP_PATH/requirements.txt

COPY . $APP_PATH
WORKDIR $APP_PATH

#RUN ["python3", "manage.py", "collectstatic", "--no-input"]

CMD ["uwsgi", "-s", "0.0.0.0:8000", "--processes", "4", "--module", "bone.wsgi"]
