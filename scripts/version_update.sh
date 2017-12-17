#!/usr/bin/env/bash

PACKAGE='keyup'
root=$(git rev-parse --show-toplevel 2>/dev/null)
HOME=$(echo $HOME)
VERSION_MODULE='_version.py'
VERSION_ORIG='_version.py.orig'

function copy_version_module(){
    local reverse=$1
    if [ $reverse ]; then
        cp -v $root/$VERSION_ORIG $root/$VERSION_MODULE
    else
        cp -v $root/$VERSION_MODULE $root/$VERSION_ORIG
    fi
}

function update_minor_version(){
        version=$(grep '__version__' $PACKAGE/_version.py  | head -n 1 | awk -F"'" '{print $2}')

        if [ -z $(echo $version | awk -F '.' '{print $3}') ]; then
            add='1'
        else
            add=$(bc -l <<< "$(echo $version | awk -F '.' '{print $3}') + 1")
        fi
        updated_version="$(echo $version | awk -F '.' '{print $1"."$2}').$add"
        echo -e "\nupdated_version number is: $updated_version\n"
        echo "__version__ = '${updated_version}'" > $root/$PACKAGE/_version.py
}


# --- main --------------------------------------------------------------------

if [ $root ]; then
    cd $root     # git repo root dir
else
    echo -e '\nrepo root not found. Exit'
    exit 1
fi

# create copy
copy_version_module

# increment version number for upload to pypi
update_minor_version

exit 0
