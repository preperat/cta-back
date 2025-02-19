#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER cta WITH SUPERUSER PASSWORD 'development_only';
    CREATE DATABASE cta OWNER cta;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "cta" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS vector;
EOSQL