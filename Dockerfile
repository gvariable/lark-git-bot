FROM python:3.11-slim
RUN pip install --upgrade pip
COPY . /root
WORKDIR /root
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "relay.py"]