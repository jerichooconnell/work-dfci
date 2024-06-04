# look at the pickle file
import pickle
import numpy as np

with open('first_layer_360_brain.pkl', 'rb') as f:
    data = pickle.load(f)

# print the source code of the function
