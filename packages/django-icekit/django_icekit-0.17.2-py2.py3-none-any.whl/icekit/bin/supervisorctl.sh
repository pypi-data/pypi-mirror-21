#!/bin/bash

set -e

exec supervisorctl --configuration "$ICEKIT_DIR/etc/supervisord.conf" "$@"
