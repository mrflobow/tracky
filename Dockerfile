FROM python:3.11
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./trackyapp /code/app

CMD ["uvicorn", "trackyapp.main:app",  "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]