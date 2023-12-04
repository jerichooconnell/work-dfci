#!/bin/bash

# num_particles=500000000

# Run ggems_edep_tests.py one time for each boolean option
python ogate_edep_tests_dli.py --body --spect --np $1 #num_particles
python ogate_edep_tests_dli.py --body --np $1 #num_particles
python ogate_edep_tests_dli.py --spect --np $1 #num_particles
python ogate_edep_tests_dli.py --np $1 #num_particles