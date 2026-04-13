FROM debian:bookworm-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pycomm3 python-dotenv

COPY src/main.py .

ENV PYTHONUNBUFFERED=1
ENV PLC_IP=192.168.1.10
ENV TAG_READ=Motor_Speed
ENV TAG_WRITE=Motor_Start
ENV POLL_INTERVAL=5

CMD ["python3", "main.py"]
