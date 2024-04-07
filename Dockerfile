FROM python:3.12.2-slim
LABEL maintainer='Vadim Kozyrevskiy', email='vadikko2@mail.ru'

ENV TZ='Europe/Moscow'

WORKDIR /code
COPY . /code

RUN apt-get update && \
    apt-get --no-install-recommends -y install gcc && \
    pip install -e .

CMD ["uvicorn", "main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "80"]
