#!/bin/bash

# num_particles=500000000

python fastcat_edep_tests.py --body -s #num_particles
python fastcat_edep_tests.py --body #num_particles
python fastcat_edep_tests.py -s #num_particles
python fastcat_edep_tests.py  #num_particles