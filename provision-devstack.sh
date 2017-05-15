#!/bin/bash
set -e

/edx/app/edxapp/devstack.sh open
./manage.py lms shell --settings devstack_docker <<EOF
# update oauth to set access token
# add integration_test.py configuration to setup
EOF