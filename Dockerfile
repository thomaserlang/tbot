FROM node:16-alpine as builder
COPY . .
RUN npm ci; npm run build


FROM python:3.9-bullseye
RUN apt-get update; apt-get upgrade -y; apt-get install curl -y
ENV \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH="${PYTHONPATH}:." \
    UID=10000 \
    GID=10001

COPY . .

RUN pip install -r requirements.txt

COPY --from=builder tbot/web/static/ui tbot/web/static/ui
COPY --from=builder tbot/web/templates/ui tbot/web/templates/ui

RUN addgroup --gid $GID --system tbot; adduser --uid $UID --system --gid $GID tbot
USER $UID:$GID
ENTRYPOINT ["python", "tbot/runner.py"]

# docker build -t thomaserlang/tbot --rm . 
# docker push thomaserlang/tbot:latest 