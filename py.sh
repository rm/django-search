#!/bin/sh

if [ ! -e env.sh ]
then
    echo "Missing env.sh"
    exit
fi

. ./env.sh
export PGPASSWORD=$BLOGAPP_DB_PASSWORD
python $*
