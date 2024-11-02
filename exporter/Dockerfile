FROM python:3.10-slim

RUN pip install poetry==1.8.4

COPY . .

COPY ./test_files/usercache.json /opt/minecraft/

COPY ./test_files/stats/ /opt/minecraft/world/stats/

RUN poetry install

WORKDIR /minecraft_prometheus_exporter

ENTRYPOINT ["poetry", "run", "python3", "-m", "main"]
