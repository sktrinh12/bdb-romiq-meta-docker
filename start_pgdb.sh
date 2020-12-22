docker run -p 5432:5432 -d \
    -e POSTGRES_USER="BDB" \
    -e POSTGRES_PASSWORD="pass" \
    -e POSTGRES_DB="metadb" \
    -v ${PWD}/pg-data:/var/lib/postgresql/data \
    --name pg-container \
    bdb_flaskapi_postgres # Docker image
