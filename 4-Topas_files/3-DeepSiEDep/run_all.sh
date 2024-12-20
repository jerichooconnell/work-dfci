#!/bin/bash

# Create the new directories and copy the contents
for new_dir in *SnBU; do
    cd $new_dir
    /home/jericho/Software/Topas/topas/bin/topas run_demo.txt
    cd ..
done