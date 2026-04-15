#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Plot addon.


set -euo pipefail


release='/usr/lib/qt6/bin/lrelease'

output='freecad/plot/Resources/Locales'
input='Resources/Locales'


releaseLocale (){

    local file=$1
    
    local source="${input}/${file}.ts"
    local target="${output}/Plot_${file}.qm"

    "$release"          \
        -nounfinished   \
        "${source}"     \
        -qm "${target}"
}


releaseLocale 'ja'
