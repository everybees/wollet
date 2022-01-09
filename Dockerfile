FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/