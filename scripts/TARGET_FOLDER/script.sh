#!/bin/bash

for referencemonitor in reference_monitor_*;
    do for testcase in vt2182_*;
        do echo "Running $testcase with $referencemonitor";
        python repy.py restrictions.default encasementlib.r2py $referencemonitor $testcase;
    done;
done
