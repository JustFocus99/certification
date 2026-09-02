#!/usr/bin/env bash

set -ex

PGPASSWORD=emailverifier psql -h localhost -p 5555 -U emailverifier postgres -c "create database registration_dev"
PGPASSWORD=emailverifier psql -h localhost -p 5555 -U emailverifier postgres -c "create database registration_test"
PGPASSWORD=emailverifier psql -h localhost -p 5555 -U emailverifier postgres -c "create database notification_dev"
PGPASSWORD=emailverifier psql -h localhost -p 5555 -U emailverifier postgres -c "create database notification_test"

./gradlew devMigrate testMigrate

# Revert any file mode changes
git diff -p -R --no-color | grep -E "^(diff|(old|new) mode)" --color=never | git apply --allow-empty
