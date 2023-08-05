#!/usr/bin/env python3
# Ducker - search with DuckDuckGo from the command line

# Copyright (C) 2017 Jorge Maldonado Ventura

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

complete -c ducker -s h -l help -f                 --description 'show help text and exit'
complete -c ducker -l version -f                   --description 'show version number and exit'
complete -c ducker -s m -l multiple-search -f      --description 'launch a search for every word given'
complete -c ducker -s i -l image-search -f         --description 'search for images'
complete -c ducker -s v -l video-search -f         --description 'search for videos'
complete -c ducker -s w -l website-search -f       --description 'search for websites'
complete -c ducker -s H -l no-javascript -f        --description 'search with DuckDuckGo html interface'
complete -c ducker -s l -l lite -f                 --description 'search with DuckDuckGo lite interface'
complete -c ducker -s s -l start -r -f             --description 'start at the Nth result'
complete -c ducker -s n -l count -r -f             --description 'show N results'
complete -c ducker -s c -l reg -r -f               --description 'region-specific search'
complete -c ducker -s x -l exact -f                --description 'disable automatic spelling correction'
complete -c ducker -s C -l nocolor -f              --description 'disable color output'
complete -c ducker -l colors -f                    --description 'set output colors'
complete -c ducker -s t -l time -f -r -a "a d w m" --description 'time limit search'
complete -c ducker -s p -l proxy -r -f             --description 'tunnel traffic through an HTTPS proxy (HOST:PORT)'
complete -c ducker -l noua -f                      --description 'disable user agent'
complete -c ducker -l json -f                      --description 'output in JSON format; implies --noprompt'
complete -c ducker -l np -l noprompt -f            --description 'perform search and exit; do not prompt'
complete -c ducker -s d -l debug -f                --description 'enable debugging'
