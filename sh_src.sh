cd "$(dirname $BASH_SOURCE)"

export PYTHONPATH=$PYTHONPATH:core/server:test

which pyenv &> /dev/null
if [ $? = 0 ]; then
    pyenv activate webchat
fi

# nvm is a shell function, not an executable
type nvm &> /dev/null
if [ $? = 0 ]; then
    nvm use v8.3.0
fi

REDIS_VERSION_ACTUAL=$(redis-cli --version | sed 's/^redis-cli //')
if [ $? != 0 ]; then
    echo "didn't find redis client installed" 1>&2
fi
REDIS_VERSION_EXPECTED='3.2.6'
if [ $REDIS_VERSION_ACTUAL != $REDIS_VERSION_EXPECTED ]; then
    echo "expected redis version $REDIS_VERSION_EXPECTED " \
         "found $REDIS_VERSION_ACTUAL" 1>&2
fi
