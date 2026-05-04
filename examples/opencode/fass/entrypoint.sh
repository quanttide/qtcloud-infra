#!/bin/sh
set -e

opencode ${OPENCODE_MODE:-serve} --hostname 0.0.0.0 --port 9000
