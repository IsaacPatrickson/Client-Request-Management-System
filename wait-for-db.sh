#!/bin/bash

echo "Waiting for Postgres to become available..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "Postgres is available."
