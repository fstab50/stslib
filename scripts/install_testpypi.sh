#!/usr/bin/env bash

VENV_PATH='~/Downloads'
VENV_DIR='p3.6_env'
PACKAGE='stsAval'


function venv(){
    local python3=$(which python3)
    #
    if [ ! $VIRTUAL_ENV ]; then
        if [ ! -d $VENV_PATH/$VENV_DIR ]; then
            python3 -m venv $VENV_PATH/$VENV_DIR
        fi
        source $VENV_PATH/$VENV_DIR/bin/activate
    fi
}

# source venv
venv

# install from test site
pip install -U awscli --extra-index-url https://test.pypi.org/simple/ $PACKAGE 
