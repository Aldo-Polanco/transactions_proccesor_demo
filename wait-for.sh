#!/bin/sh
while true; do  
    if nc -z db 5432; then
        echo "db is up";
        python database_schema_generator.py;
        break;
    else
        echo "db is not yet reachable; sleep for 3s before retry";
        sleep 3;
    fi 
done
exec "$@"
