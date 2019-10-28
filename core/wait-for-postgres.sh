#!/bin/sh
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

attempts=0;
until python -c "import psycopg2; psycopg2.connect(\"dbname=headway user=postgres host=${POSTGRES_HOST} password=${POSTGRES_PASSWORD}\")" &> /dev/null;
do
  >&2 echo "Postgres is unavailable - sleeping"

  attempts = $((attempts + 1 ));
  give_up = $((attempts == 30));

  >&2 echo "Postgres is unavailable - sleeping (${attempts}/30)"

  if [ $give_up = "1" ] ; then
      >&2 echo "Cannot connect to the postgres server after 30 seconds; exiting";
      exit;
  fi;

  sleep 1
done

>&2 echo "Postgres is up - executing command ${cmd}"
exec $cmd
