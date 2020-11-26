#!/bin/bash

read -e -p "Enter filename with structure contents: " filename
grep structuredet: ${filename} | cut -c 15- > ${filename/.out/.dat}