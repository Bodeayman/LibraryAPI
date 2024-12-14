FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN python -m venv venv

RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt

EXPOSE 3000

ENV FLASK_APP=library.py
ENV FLASK_ENV=development

CMD ["./venv/bin/python", "library.py"]
