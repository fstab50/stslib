#!/usr/bin/env bash


VENV_PATH=$(echo $HOME)/Downloads
VENV_DIR='p3.6_venv'
PACKAGE='stsAval'


function venv(){
    local python3=$(which python3)
    #
    if [ ! $VIRTUAL_ENV ]; then
        if [ ! -d $VENV_PATH/$VENV_DIR ]; then
            echo -e "\nchanging to $VENV_PATH..."
            cd $VENV_PATH
            python3 -m venv $VENV_DIR
        fi
        echo -e "\nSourcing venv $VENV_DIR..."
        source $VENV_PATH/$VENV_DIR/bin/activate
    fi
}
# source venv
venv
exit 0
# install from test site
pip install -U awscli --extra-index-url https://test.pypi.org/simple/ $PACKAGE 


