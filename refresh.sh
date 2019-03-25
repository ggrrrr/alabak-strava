#!/bin/bash

DB_USER=$1
DB_PASS=$2
DB_HOST=$3

python3 src/python/cli.py --pgUser ${DB_USER} --pgPassword ${DB_PASS} --pgPort ${DB_HOST} --cmd refreshToken --level error
# python3 src/python/cli.py --accessToken c148787f5e2947265b790b79e3b8a22000bc9abe  --cmd refreshToken --clientId 32757 --clientSecret 8f0cdd6970f42f99e40eed261ad9ba88ba32a243 --refreshToken 92cde50627f40d5496f1203ce734caa484d38c99

