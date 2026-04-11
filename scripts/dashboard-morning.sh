#!/bin/bash
set -e

export PATH="/usr/local/bin:/usr/bin:/bin"
cd /home/michal/displaypi

/usr/bin/just sync
/usr/bin/just display-morning-today