#!/bin/bash -e

IMAGE="xeon-ubuntu1604-analytics-ffmpeg"
DIR=$(dirname $(readlink -f "$0"))

. "${DIR}/../../../script/shell.sh"
