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

cp -r bower_components \
    style \
    js \
    index.html \
    $DEST_DIR

if [ -f $DEST_DIR/js/config/server.js ]
then
		rm $DEST_DIR/js/config/server.js
fi

case $DEPLOY_DEST in
    "local")
				cp js/config/server_local.js \
						$DEST_DIR/js/config/server.js
        ;;
    "remote")
				cp js/config/server_remote.js \
						$DEST_DIR/js/config/server.js
        ;;
    *)
        echo "unknown deploy destination" 1>&2
        exit 1
        ;;
esac

