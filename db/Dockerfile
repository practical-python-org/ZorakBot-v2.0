FROM postgres

ENV POSTGRES_DB your_database_name
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD your_password

# Expose the default PostgreSQL port
EXPOSE 5432
COPY ./scripts/ /docker-entrypoint-initdb.d/

# CMD instruction to start PostgreSQL
CMD ["postgres"]