#! /bin/sh

if [ $# != 2 ]
then
    echo "provide destination directory for client build" 1>&2
    echo "and specify deploy destination" 1>&2
    exit 1
fi

DEST_DIR=$1

if [ ! -d $DEST_DIR ]
then
    echo "$1 is not a directory" 1>&2
    exit 1
fi

DEPLOY_DEST=$2

case $DEPLOY_DEST in
    "local")
        echo "local deploy"
        ;;
    "remote")
        echo "remote deploy"
        ;;
    *)
        echo "unknown deploy destination" 1>&2
        exit 1
        ;;
esac

cp -r bower_components \
    style \
    js \
    index.html \
    $DEST_DIR

