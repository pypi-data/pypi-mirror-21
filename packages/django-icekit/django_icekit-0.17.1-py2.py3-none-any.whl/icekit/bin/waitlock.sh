#!/bin/bash

# Execute cronlock in a loop to queue but avoid overlaps, instead of exiting
# when a lock is already acquired.

# Don't use Redis locks to serialize access to shared resources, e.g. database.
if [[ -z "$WAITLOCK_ENABLE" ]]; then
	exec "$@"
fi

cat <<EOF
# `whoami`@`hostname`:$PWD$ waitlock.sh $@
EOF

set -e

export CRONLOCK_GRACE="${CRONLOCK_GRACE:-0}"
export CRONLOCK_HOST="${CRONLOCK_HOST:-localhost}"
export CRONLOCK_RELEASE="${CRONLOCK_RELEASE:-3600}"

COUNT=0
while true; do
	cronlock.sh "$@" && STATUS="$?" || STATUS="$?"
	if [[ "$STATUS" == 200 ]]; then
		if [[ "$COUNT" == 0 ]]; then
			echo "Waiting to acquire lock for command: $@"
		fi
		(( COUNT += 1 ))
		sleep 1
		continue
	fi
	break
done

if (( COUNT > 0 )); then
	echo "Waited $COUNT seconds to acquire lock for command: $@"
fi

exit "$STATUS"
