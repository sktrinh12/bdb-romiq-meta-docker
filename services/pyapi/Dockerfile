FROM python:3.8.1-slim-buster

ARG HOSTNAME
ARG UNAME
ARG PASSWORD
ENV UNAME $UNAME
ENV PASSWORD $PASSWORD
ENV HOSTNAME $HOSTNAME
ENV TZ America/Los_Angeles

# prevents pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# prevents buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install -y openssh-server sudo netcat curl

RUN useradd "${UNAME}" \
    && echo "${UNAME}:${PASSWORD}" | chpasswd

ENV HOME=/home/"${UNAME}"
ENV APP_HOME=/home/"${UNAME}"/pyapi
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME
EXPOSE 22

RUN pip install --upgrade pip

COPY ./services/pyapi .
RUN pip install -r requirements.txt
RUN chown -R ${UNAME}:${UNAME} $APP_HOME
RUN chmod +x $APP_HOME/pyapi_startup.sh
USER "${UNAME}"
# ENTRYPOINT ["sh", "/home/bdb/pyapi/pyapi_startup.sh"]
