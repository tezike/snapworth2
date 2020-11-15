FROM ubuntu:18.04

RUN apt update /
    apt install -y python3 python3-pip

WORKDIR /app

COPY . /app

RUN pip3 install --upgrade pip

#RUN pip3 install -r requirements.txt

#execute an editable installation
RUN pip3 install -e .

EXPOSE 8000

ENTRYPOINT \bin\bash -c "uvicorn snapworth.app:app --reload --workers 4 --host 0.0.0.0 --port 8000"