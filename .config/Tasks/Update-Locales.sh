#!/usr/bin/env bash


update='/usr/lib/qt6/bin/lupdate'

files=($(find "freecad" $ -name "*.ui" -o -name "*.py" ))

"$update" "${files[@]}" \
    -ts 'Resources/Locales/Base.ts'


"$update" "${files[@]}"                         \
    -source-language en_US                      \
    -target-language jp                         \
    -ts 'Resources/Locales/jp.ts'