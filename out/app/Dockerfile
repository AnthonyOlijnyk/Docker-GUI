FROM nvidia/cuda:10.2-base
WORKDIR /app
COPY requirements.txt ./
RUN apt-get -y update && apt-get -y install python3.6 python3-pip \
    && pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt
COPY . .
