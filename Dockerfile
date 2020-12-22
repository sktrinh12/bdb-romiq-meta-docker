FROM postgres:latest

RUN apt-get update -y
RUN apt-get install -y postgresql-server-dev-10 gcc musl-dev
USER postgres
EXPOSE 5432
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
