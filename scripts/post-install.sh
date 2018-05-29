#!/usr/bin/env bash

#
# Post-Install Script: keyup 
#

# globals
CUR_DIR=$(pwd)
SCRIPTS_DIR="$CUR_DIR/scripts"
facility='local17'
$log=$(which logger)

# source deps
source "$SCRIPTS_DIR/colors.sh"


# --- declarations ------------------------------------------------------------


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
        printf '%*s\n\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' _
        echo -e "\n${yellow}[ $cyan$pref$yellow ]$reset  $msg\n" | indent04
    else
        echo -e "\n${yellow}[ $cyan$pref$yellow ]$reset  $msg\n" | indent04
    fi
}



# --- main ---------------------------------------------------------------------


# --- determine which system logger used ---#


if [ $(which rsyslog) ]; then
    LOGGER="rsyslog"    
    # configure rsyslog facility
    echo -e '\n# added by keyup installer' >> /etc/rsyslog.d/50-default.conf 
    echo -e 'local7.*      -/var/log/keyup.log' >> /etc/rsyslog.d/50-default.conf 
    
elif [ $(which syslog-ng) ]; then
    LOGGER="syslog-ng"
    # configure syslog-ng facility

elif [ $(which syslog) ]; then
    LOGGER="syslog"
    # configure syslog facility
fi


# --- determine init system  ---#


if [ $(which systemctl) ]; then
    # init = systemd
    INIT_BIN=$(which systemctl)
    RESTART_LOGGER="$INIT_BIN restart $LOGGER"

elif [ $(which service?) ]; then
    # init = upstart
    
elif [ $(which /etc/init.d) ]; then
    # init = init.d

fi

# restart logger
$RESTART_LOGGER

# test configuration
$log -p "$facility.info" "keyup installer test message"

# confirm test results
if [ $(grep keyup /var/log/keyup.log) ]; then

    msg="[INFO]: keyup post installation completed successfully"
    $log -p "$facility.info" "$msg"
    std_message "$msg" INFO
else
    std_message "keyup post installation was unable to configure system logger" WARN
fi


# --- end ---#
exit 0


