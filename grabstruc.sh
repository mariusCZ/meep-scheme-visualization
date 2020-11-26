#!/bin/bash

read -e -p "Enter filename of the simulation " filename
mpirun meep $filename > struc.out &
child_pid=$!
echo $child_pid

echo "Wait for simulation to initialize..."
while kill -0 $child_pid >/dev/null 2>&1; do
    word="$(awk '{w=$1} END{print w}' struc.out)"
	if [[ $word == "on" ]]; then
		kill -9 $child_pid
	fi
    sleep 1
done

echo "Done."

grep structuredet: struc.out | cut -c 15- > struc.dat

python3 visualize.py --fname ${filename/.ctl/-eps-000000.00.h5} --pname struc.dat