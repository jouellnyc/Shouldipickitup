#!/bin/bash
cd /shouldipickitup
/usr/local/bin/gunicorn -b 0.0.0.0:8000 flask:app -w 4 --access-logfile access.log
