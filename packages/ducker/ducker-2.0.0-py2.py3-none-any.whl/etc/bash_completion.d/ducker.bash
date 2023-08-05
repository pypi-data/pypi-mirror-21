#!/usr/bin/env python3
# Ducker - search with DuckDuckGo from the command line

# Copyright (C) 2016-2017 Jorge Maldonado Ventura

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

_ducker() {
    COMPREPLY=()
    local IFS=$' \n'
    local cur=$2 prev=$3
    local -a opts opts_with_args
    opts=(
        -h --help
        --version
        -m --multiple-search
        -w --website-search
        -H --no-javascript
        -l --lite
        -i --image-search
        -v --video-search
        -x --exact
        -C --nocolor
        --noua
        --json
        --np --noprompt
        -d --debug
        --colors
        -t --time
        -c --reg
        --site
        -p --proxy
        -s --start
        -n --count
    )
    opts_with_args=(
        --colors
        -t --time
        -c --reg
        --site
        -p --proxy
        -s --start
        -n --count
    )

    # Do not complete non option names
    [[ $cur == -* ]] || return 1

    # Do not complete when the previous arg is an option expecting an argument
    for opt in "${opts_with_args[@]}"; do
        [[ $opt == $prev ]] && return 1
    done

    # Complete option names
    COMPREPLY=( $(compgen -W "${opts[*]}" -- "$cur") )
    return 0
}

complete -F _ducker ducker
