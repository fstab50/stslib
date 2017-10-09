#!/usr/bin/env/bash

PACKAGE='stsaval'
root=$(git rev-parse --show-toplevel 2>/dev/null)
wkdir="/home/blake/Downloads"

if [ $root ]; then
    cd $root     # git repo root dir
else
    echo -e '\nrepo reoot not found. Exit'
    exit 1
fi

# convert readme to required
pandoc --from=markdown --to=rst --output=README.rst README.md

# build source dist
python3 setup.py sdist

# build python3-spec wheel
python3 setup.py bdist_wheel

# upload
twine upload --repository testpypi dist/*

# install
echo -e "\n"
read -p "do you want to install $PACKAGE now? [quit]" CHOICE
echo -e "\n"

if [ -z $CHOICE ]; then
    exit 0
else
    read -p "which version to install? [latest]" CHOICE2
    if [ -z $CHOICE2 ]; the
        # version required or test.pypi breaks
        version=$(grep '__version__' $PACKAGE/_version.py  | head -n 1 | awk -F"'" '{print $2}')
        pip install -U --extra-index-url https://test.pypi.org/simple/  $PACKAGE==$version
    else
        pip install -U --extra-index-url https://test.pypi.org/simple/  $PACKAGE=="$CHOICE2"
    fi
fi

exit 0
