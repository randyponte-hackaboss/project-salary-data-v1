FROM python:3.11.4
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY /src /src
COPY /cache /cache
WORKDIR /src
ENV FLASK_ENV=development
ENV NGRAMS=2
ENV CACHE_PATH=../cache/cache.pkl
ENV OVERLAPS_CONTEXT_THRESHOLD=0.5
ENTRYPOINT flask --app api.py run -p 3000 --host=0.0.0.0