FROM python:3.12

WORKDIR /code

COPY . .

RUN pip install .

CMD ["uvicorn", "eventsapi.main:app", "--host", "0.0.0.0", "--port", "80", "--timeout-keep-alive", "120"]
