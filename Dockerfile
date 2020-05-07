FROM python:3.8

RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /app

COPY ./Pipfile* ./

RUN pipenv install

ENV PYTHONPATH=/app

COPY ./run.py .
COPY ./resources ./resources

CMD ["pipenv", "run", "python", "run.py"]