FROM postgres:latest
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ENV POSTGRES_USER $POSTGRES_USER
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD
ENV POSTGRES_DB $POSTGRES_DB
ENV DEBIAN_FRONTEND noninteractive

USER root
RUN apt-get update -y
RUN apt-get install -y postgresql-server-dev-10 gcc musl-dev
COPY services/postgres/create_table.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
