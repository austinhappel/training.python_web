#!/bin/bash

CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export DJANGO_SETTINGS_MODULE="djangor.settings_production"
export DJANGO_WEB_ROOT="/var/www/sites/week06-djangor/webroot"