#
FROM python:3.9

# install system dependencies
# RUN apt-get update \
#     && apt-get -y install gcc make \
#     && rm -rf /var/lib/apt/lists/*s

WORKDIR /code

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
#RUN apt-get install -y libzbar0
COPY ./requirements.txt /code/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /code/requirements.txt


COPY ./app /code/app

CMD ["gunicorn", "app.main:app", "--workers 3","--worker-class","uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:3000:3000"]
