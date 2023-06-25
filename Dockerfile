FROM node:16-alpine as jsbuilder
COPY . .
RUN npm ci; npm run build


FROM python:3.10-bookworm as pybuilder
COPY . .
RUN pip wheel -r requirements.txt --wheel-dir=/wheels
RUN pip wheel mysqlclient==2.1.0 --wheel-dir=/wheels


FROM python:3.10-slim-bookworm
RUN apt-get update; apt-get upgrade -y; apt-get install curl -y
ENV \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH="${PYTHONPATH}:." \
    UID=10000 \
    GID=10001

COPY . .

COPY --from=pybuilder /wheels /wheels
RUN pip install --no-index --find-links=/wheels -r requirements.txt

COPY --from=jsbuilder tbot/web/static/ui tbot/web/static/ui
COPY --from=jsbuilder tbot/web/templates/ui tbot/web/templates/ui

RUN addgroup --gid $GID --system tbot; adduser --uid $UID --system --gid $GID tbot
USER $UID:$GID
ENTRYPOINT ["python", "tbot/runner.py"]

# docker build -t thomaserlang/tbot --rm . 
# docker push thomaserlang/tbot:latest 