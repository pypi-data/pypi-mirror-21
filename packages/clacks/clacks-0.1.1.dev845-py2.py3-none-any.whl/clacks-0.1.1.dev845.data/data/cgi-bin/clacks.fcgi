#!/bin/sh
THISFILE=$(readlink -f $(which $0) 2>/dev/null)
CLACKS_PATH=${CLACKS_PATH:=$(readlink -f "$(dirname "$THISFILE")/..")}
export CLACKS_PATH
GTOOL_ENVPATH=$CLACKS_PATH
export GTOOL_ENVPATH
#important below is UTF-8 needed by filename handling os module code
export LANG=en_US.UTF-8
PATH="$BASEPATH/bin:$PATH"
export PATH

exec $CLACKS_PATH/bin/python3 $CLACKS_PATH/bin/clacks -f
