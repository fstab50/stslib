#!/usr/bin/env/bash

PACKAGE='stslib'
root=$(git rev-parse --show-toplevel 2>/dev/null)
HOME=$(echo $HOME)


function update_minor_version(){
        version=$(grep '__version__' $PACKAGE/_version.py  | head -n 1 | awk -F"'" '{print $2}')

        if [ -z $(echo $version | awk -F '.' '{print $4}') ]; then
            add='1'
        else
            add=$(bc -l <<< "$(echo $version | awk -F '.' '{print $4}') + 1")
        fi
        updated_version="$(echo $version | awk -F '.' '{print $1"."$2"."$3}').$add"
        echo -e "\nupdated_version number is: $updated_version\n"
        echo "__version__ = '${updated_version}'" > $root/stslib/_version.py
}


# --- main --------------------------------------------------------------------


if [ $root ]; then
    cd $root     # git repo root dir
else
    echo -e '\nrepo root not found. Exit'
    exit 1
fi

# convert readme to required
pandoc --from=markdown --to=rst --output=README.rst README.md

# build source dist
python3 setup.py sdist

# build python3-spec wheel
python3 setup.py bdist_wheel

# upload
twine upload --repository pypi dist/*

exit 0
