#! /bin/sh

if [ $# != 1 ]
then
    echo "provide destination directory for client build" 1>&2
    exit 1
fi

DEST_DIR=$1

if [ ! -d $DEST_DIR ]
then
    echo "$1 is not a directory" 1>&2
    exit 1
fi

cp -r bower_components \
    style \
    js \
    index.html \
    $DEST_DIR
