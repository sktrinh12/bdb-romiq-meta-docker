FROM python:3.8.1-slim-buster

ARG HOSTNAME
ARG DBNAME
ARG PORT
ARG UNAME
ARG PASSWORD
ENV UNAME $UNAME
ENV PASSWORD $PASSWORD
ENV DBNAME $DBNAME
ENV PORT $PORT
ENV HOSTNAME $HOSTNAME
ENV TZ America/Los_Angeles
# ENV WKDIR /usr/src/app

# prevents pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# prevents buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install -y openssh-server sudo netcat curl

# RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 "${UNAME}"
RUN useradd "${UNAME}" \
    && echo "${UNAME}:${PASSWORD}" | chpasswd

# WORKDIR /usr/src/app
ENV HOME=/home/"${UNAME}"
ENV APP_HOME=/home/"${UNAME}"/pyapi
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME
EXPOSE 22

RUN pip install --upgrade pip
# COPY ./services/pyapi/requirements.txt "${WKDIR}"/requirements.txt

COPY ./services/pyapi .
RUN pip install -r requirements.txt
RUN chown -R ${UNAME}:${UNAME} $APP_HOME
RUN chmod +x $APP_HOME/pyapi_startup.sh
USER "${UNAME}"
ENTRYPOINT ["sh", "/home/bdb/pyapi/pyapi_startup.sh"]
