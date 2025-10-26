#!/usr/bin/env bash

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
        -ts "${file}"
}


updateLocale 'ja'
