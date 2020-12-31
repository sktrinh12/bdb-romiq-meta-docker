#!/bin/bash
service ssh start
/usr/sbin/sshd -D
echo "Waiting for postgres..."
while ! nc -z postgres 5432; do
    sleep 0.1
done
echo "PostgreSQL started"
# python manage.py run -h 0.0.0.0 #already calling in docker-compose
exec "$@"
