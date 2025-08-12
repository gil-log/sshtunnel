FROM python:3.10-slim

RUN pip install sshtunnel

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["python", "-u", "/entrypoint.py"]
