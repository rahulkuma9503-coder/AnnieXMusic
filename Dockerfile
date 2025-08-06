FROM nikolaik/python-nodejs:python3.10-nodejs20

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir --upgrade -r requirements.txt

# Add this to your Dockerfile if exists
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:$PORT/ || exit 1

CMD bash start
