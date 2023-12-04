#!/bin/bash

# num_particles=500000000

# Run ggems_edep_tests.py one time for each boolean option
python gate_edep_tests.py --body --spect --np $1 #num_particles
python gate_edep_tests.py --body --np $1 #num_particles
python gate_edep_tests.py --spect --np $1 #num_particles
python gate_edep_tests.py --np $1 #num_particles