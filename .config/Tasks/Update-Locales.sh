#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Plot addon.


set -euo pipefail


update='/usr/lib/qt6/bin/lupdate'

output='Resources/Locales'


files=($( find "freecad" -name "*.ui" -o -name "*.py" ))


updateLocale (){

    local locale=$1
    
    local file="${output}/${locale}.ts"

    "$update" "${files[@]}"                         \
        -source-language en_US                      \
        -target-language "${locale}"                \
        -no-obsolete                                \
        -ts "${file}"
}


updateLocale 'ja'
