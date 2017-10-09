#!/usr/bin/env bash

#------------------------------------------------------------------------------
#
# AUTHOR:  Blake Huber
#
# SYNOPSIS:
#   this script is used to perform stsAval source build
#   and upload to test pypi and pypi
#
# REQUIREMENTS:
#   - python v3.5, v3.6
#   - ubuntu linux v14.04+, Redhat v6+
#   - modules setuptools, twine, wheel
#
#------------------------------------------------------------------------------

TEST='testpypi'
PROD='pypi'
VENV_PATH='~/Downloads'
VENV_DIR='p3_env'

# error codes
E_DEPENDENCY=1        # exit code if missing required dependency
E_DIR=2               # exit code if failure to create log dir, log file
E_BADSHELL=3          # exit code if incorrect shell detected
E_AUTHFAIL=5          # exit code if authentication failure
E_BADPROFILE=6        # exit code if profile name/ role not found in local config
E_USER_CANCEL=7       # exit code if user cancel
E_BADARG=8            # exit code if bad input parameter
E_EXPIRED_CREDS=9     # exit code if temporary credentials no longer valid
E_MISC=11             # exit code if miscellaneous (unspecified) error

# Formatting
blue=$(tput setaf 4)
cyan=$(tput setaf 6)
green=$(tput setaf 2)
purple=$(tput setaf 5)
red=$(tput setaf 1)
white=$(tput setaf 7)
yellow=$(tput setaf 3)
orange='\033[0;33m'
gray=$(tput setaf 008)
lgray='\033[0;37m'                  # light gray
dgray='\033[1;30m'                  # dark gray
reset=$(tput sgr0)
#
BOLD=`tput bold`
UNBOLD=`tput sgr0`

#
### -- functions declarations  ----------------------------------------------###
#

# formatting
function indent02() { sed 's/^/  /'; }
function indent10() { sed 's/^/          /'; }

function help_menu(){
    cat <<EOM

  Help Contents
  -------------

    $  sh ${BOLD}build.sh${UNBOLD} --env <${yellow}test${reset}> | <${yellow}prod${reset}>

            [ test : ${white}testpypi${reset}    ]
            [ prod :  ${red}pypi${reset}    ]


EOM
    #
    # <<-- end function help_menu -->>
}

function parse_parameters(){
    if [[ ! $@ ]]; then
        help_menu
        exit 0
    else
        while [ $# -gt 0 ]; do
            case $1 in
                -e | --env)
                    if [ $2 == "test" ]; then
                        environment=$TEST
                    elif [ $2 == 'prod']; then
                        environment=$PROD
                    fi
                    std_message "Upload environment set to: $environment"
                    shift 2
                    ;;
                -h | --help)
                    help_menu
                    shift 1
                    exit 0
                    ;;
                *)
                    help_menu
                    msg="Unrecognized argument [ $1 ] given. Exiting (code $E_BADARG)"
                    std_error_exit "$msg" $E_BADARG
                    ;;
            esac
        done
    fi
    #
    # <<-- end function parse_parameters -->>
}

function convert_readme(){
    cd $root
    if [ ! "README.rst" ]; then
        pandoc --from=markdown --to=rst --output="README.rst" "README.md"
    fi
}

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

function std_message(){
    local msg="$1"
    #std_logger "[INFO]: $msg"
    [[ $quiet ]] && return
    shift
    pref="----"
    if [[ $1 ]]; then
        pref="${1:0:4}"
        shift
    fi
    echo -e "\n${yellow}[ $cyan$pref$yellow ]$reset  $msg\n" | indent02
}

function std_error(){
    local msg="$1"
    #std_logger "[ERRR]: $msg"
    echo -e "\n${yellow}[ ${red}ERRR${yellow} ]$reset  $msg\n" | indent02
}

function std_error_exit(){
    local msg="$1"
    local status="$2"
    std_error "$msg"
    exit $status
}

function binary_depcheck(){
    ## validate binary dependencies installed
    local check_list=( "$@" )
    local msg
    #
    for prog in "${check_list[@]}"; do
        if ! type "$prog" > /dev/null 2>&1; then
            msg="$prog is required and not found in the PATH. Aborting (code $E_DEPENDENCY)"
            std_error_exit "$msg" $E_DEPENDENCY
        fi
    done
    #
    # <<-- end function binary_depcheck -->>
}

function python_version_depcheck(){
    ## dependency check for a specific version of python binary ##
    local version
    local version_min="$1"
    local version_max="$2"
    local msg
    #
    local_bin=$(which python3)
    # determine binary version
    version=$($local_bin 2>&1 --version | awk '{print $2}' | cut -c 1-3)
    #
    if (( $(echo "$version > $version_max" | bc -l) )) || \
       (( $(echo "$version < $version_min" | bc -l) ))
    then
        msg="python version $version detected - must be > $version_min, but < $version_max"
        std_error_exit "$msg" $E_DEPENDENCY
    fi
    #
    # <<-- end function python_depcheck -->>
}

function python_module_depcheck(){
    ## validate python library dependencies
    local check_list=( "$@" )
    local msg
    #
    for module in "${check_list[@]}"; do
        exitcode=$(python3 -c "import $module" > /dev/null 2>&1; echo $?)
        if [[ $exitcode == "1" ]]; then
            # module not imported, not found
            msg="$module is a required python library. Aborting (code $E_DEPENDENCY)"
            std_error_exit "$msg" $E_DEPENDENCY
        fi
    done
    #
    # <<-- end function python_module_depcheck -->>
}

function depcheck(){
    ## validate dependencies ##
    local logging=$1
    local msg
    #
    ## test default shell ##
    if [ ! -n "$BASH" ]; then
        # shell other than bash
        msg="Default shell appears to be something other than bash. Please rerun with bash. Aborting (code $E_BADSHELL)"
        std_error_exit "$msg" $E_BADSHELL
    fi

    ## log dir ##
    if [ $logging ]; then
        if [[ ! -d $pkg_path/logs ]]; then
            if ! mkdir -p "$pkg_path/logs"; then
                msg="$pkg: failed to make log directory: $pkg_path/logs"
                std_error_exit "$msg" $E_DIR
            fi
        fi
    fi

    # set repository root
    root=$(git rev-parse --show-toplevel 2>/dev/null)
    if [ ! $root ]; then
        std_error_exit "Not located in git repository, root not found" $E_DEPENDENCY
    fi
    ## check for required cli tools ##
    binary_depcheck "awk" "cut" "grep" "bc" "python3" "pandoc" "git"

    ## check python version ##
    python_version_depcheck "3.5" "3.6"

    # check aws python sdk available
    python_module_depcheck "twine" "wheel" "setuptools"
    #
    # <<-- end function depcheck -->>
}

function clean_up(){
    #
    cd $root
    if [ -d dist ]; then
        rm -fr dist
        rm -fr *.egg-info
    fi
    if [ -e 'README.rst' ]; then
        rm -f "README.rst"
    fi
}

#
### -- main -----------------------------------------------------------------###
#

# validate dependencies and inputs
std_message "checking dependencies" INFO
depcheck
parse_parameters $@

cd $root

# create, start venv
std_message "venv setup" INFO
venv

# prep
clean_up

# create readme for upload
std_message "converting readme" INFO
convert_readme

# build source in virtualenv
std_message "running setup.py" INFO
python setup.py sdist

# upload
std_message "uploading to $environment" INFO
twine upload --repository $environment dist/*

clean_up
