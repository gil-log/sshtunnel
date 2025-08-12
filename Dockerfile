FROM python:3.10-slim

RUN pip install "paramiko<3.0" sshtunnel

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["python", "-u", "/entrypoint.py"]
