#!/usr/bin/env bash

chmod o+rwx $CLOUDSDK_CONFIG
su-exec $UID:$GID "$@"