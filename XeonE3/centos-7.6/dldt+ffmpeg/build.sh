#!/bin/bash -e

IMAGE="xeone3-centos76-analytics-ffmpeg"
VERSION="1.0"
DIR=$(dirname $(readlink -f "$0"))

. "${DIR}/../../../script/build.sh"
