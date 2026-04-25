#!/usr/bin/env bash
set -e

sudo docker run --rm \
  --privileged \
  -v /dev:/dev \
  -v /run/udev:/run/udev:ro \
  displaypi "$@"
