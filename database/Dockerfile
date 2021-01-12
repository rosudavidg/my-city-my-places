# Postgres base image
FROM postgres:12

# Copy init scripts
COPY ./init-scripts/ /docker-entrypoint-initdb.d/

# Expose default port for postgres
EXPOSE 5432
