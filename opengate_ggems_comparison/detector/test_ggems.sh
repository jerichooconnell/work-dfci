#!/bin/bash

#Make it so that the scipts takes num_particles as an argument
# num_particles=$1
#Make a variable for the number of particles
# num_particles=100000

# Run ggems_edep_tests.py one time for each boolean option
python ggems_edep_tests_dli.py --body --spect --np $1 #num_particles
python ggems_edep_tests_dli.py --body --np $1 #num_particles
python ggems_edep_tests_dli.py --spect --np $1 #num_particles
python ggems_edep_tests_dli.py --np $1 #num_particles
