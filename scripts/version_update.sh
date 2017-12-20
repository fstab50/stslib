#!/usr/bin/env/bash

PACKAGE='stsAval'
HOME=$(echo $HOME)
PIP_CALL=$(which pip3)
GIT=$(which git)
ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
VERSION_MODULE='_version.py'

# Formatting
cyan=$(tput setaf 6)
white=$(tput setaf 7)
yellow=$(tput setaf 3)
reset=$(tput sgr0)
BOLD=`tput bold`
UNBOLD=`tput sgr0`

#
# Logic:
#   - extract version if package installed local
#   - not found, searches pip repo for package, extracts version
#   - increments local version from package module
#

# --- declarations  ------------------------------------------------------------

# indent
indent02() { sed 's/^/  /'; }
indent04() { sed 's/^/    /'; }

function restore_version(){
    $GIT checkout "$PACKAGE/$VERSION_MODULE"
}

function get_current_version(){
    ## gets current version of package in pypi or testpypi ##

    # check if installed locally
    pip_local=$($PIP_CALL list | grep $PACKAGE  | awk '{print $2}')

    # use package version if not installed in pypi
    if [ -z $pip_local ]; then
        # search pip repo
        pip_search=$($PIP_CALL search $PACKAGE | awk -F '(' '{print $2}' | awk -F ')' '{print $1}')

        if [ -z $pip_search ]; then
            # use local version module in package
            restore_version
            std_message "Using version found in ${yellow}$PACKAGE${reset} version module." INFO
            version=$(grep '__version__' $PACKAGE/_version.py  | head -n 1 | awk -F"'" '{print $2}')
        else
            std_message "Using version number from search of pip repository." INFO
            version=$pip_search
        fi
    else
        std_message "Using pip installed version number." INFO
        version=$pip_local
    fi
}

function update_minor_version(){
    ## increment minor version ##
    if [ $version ]; then
        if [ -z $(echo $version | awk -F '.' '{print $3}') ]; then
            add='1'
        else
            add=$(bc -l <<< "$(echo $version | awk -F '.' '{print $3}') + 1")
        fi
        updated_version="$(echo $version | awk -F '.' '{print $1"."$2}').$add"
        std_message "Updated_version number is: ${BOLD}$updated_version${UNBOLD}" INFO
        echo "__version__ = '${updated_version}'" > $ROOT/$PACKAGE/_version.py
    else
        echo -e "\nNo version number identified. Abort\n"
    fi
}

function std_message(){
    local msg="$1"
    local format="$3"
    #
    #std_logger "[INFO]: $msg"
    [[ $quiet ]] && return
    shift
    pref="----"
    if [[ $1 ]]; then
        pref="${1:0:5}"
        shift
    fi
    if [ $format ]; then
        echo -e "${yellow}[ $cyan$pref$yellow ]$reset  $msg" | indent04
    else
        echo -e "\n${yellow}[ $cyan$pref$yellow ]$reset  $msg\n" | indent04
    fi
}


# --- main --------------------------------------------------------------------

if [ $ROOT ]; then
    cd $ROOT     # git repo ROOT dir
else
    echo -e '\nrepo ROOT not found. Exit'
    exit 1
fi

# current installed version
get_current_version

# increment version number for upload to pypi
update_minor_version

exit 0
