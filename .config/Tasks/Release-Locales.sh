#!/usr/bin/env bash


release='/usr/lib/qt6/bin/lrelease'


releaseLocale (){

    local file=$1
    
    local source="Resources/Locales/${file}.ts"
    local target="freecad/plot/Resources/Locales/${file}.qm"

    "$release"          \
        -nounfinished   \
        "${source}"     \
        -qm "${target}"
}


releaseLocale 'Base'
releaseLocale 'jp'
