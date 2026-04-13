FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pycomm3

COPY src/main.py .

ENV PYTHONUNBUFFERED=1
ENV PLC_IP=192.168.1.20
ENV TAG_READ=Motor_Speed
ENV TAG_WRITE=Motor_Start
ENV POLL_INTERVAL=5

CMD ["python", "main.py"]
