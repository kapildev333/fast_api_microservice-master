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

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && apt-get install -y build-essential libzbar-dev 
RUN apt-get install -y libzbar0
COPY ./requirements.txt /code/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /code/requirements.txt


COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "3000"]
