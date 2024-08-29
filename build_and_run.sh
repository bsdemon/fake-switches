#!/bin/bash

docker build -t fake_switches .
docker run --name fake_olt -d -p -e SWITCH_MODEL=cisco_2960_48TT_L fake_switches
